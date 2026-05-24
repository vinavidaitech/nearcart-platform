import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.accounts.models import CustomUser
from apps.inventory.models import Product, ProductVariant, StockMovement
from apps.shops.models import Shop


# ── Supplier ───────────────────────────────────────────────────────────────────


class Supplier(models.Model):
    """
    Vendor / distributor that your shop restocks from.
    Scoped to a shop so each owner manages their own supplier list.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="suppliers")
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    gstin = models.CharField(max_length=20, blank=True)  # India GST-IN
    payment_terms_days = models.PositiveSmallIntegerField(default=30)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_supplier"
        unique_together = [("shop", "name")]

    def __str__(self):
        return f"{self.name} ({self.shop.name})"


# ── Customer ───────────────────────────────────────────────────────────────────


class Customer(models.Model):
    """
    Represents a buyer in context of a shop.
    May be linked to a CustomUser (registered) or be a walk-in profile.
    One user can be a "customer" at multiple shops (no unique_together on user alone).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="customers")
    # Optional link to a registered platform user
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shop_customer_profiles",
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, db_index=True)
    email = models.EmailField(blank=True)
    gstin = models.CharField(max_length=20, blank=True)  # B2B customers
    address = models.TextField(blank=True)
    # Running loyalty / credit balance (positive = credit owed to customer)
    loyalty_points = models.PositiveIntegerField(default=0)
    credit_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_customer"
        indexes = [
            models.Index(fields=["shop", "phone"]),
            models.Index(fields=["shop", "user"]),
        ]

    def __str__(self):
        return f"{self.name} — {self.shop.name}"


# ── Tax configuration ──────────────────────────────────────────────────────────


class TaxRate(models.Model):
    """
    Named tax slabs applicable per shop (e.g. GST 5%, GST 18%, VAT 10%).
    Applied at the line-item level on Sales/Purchase orders.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="tax_rates")
    name = models.CharField(max_length=100)  # "GST 18%", "Zero Rated"
    rate = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0"))],
    )  # 0.18 = 18 %
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "billing_taxrate"
        unique_together = [("shop", "name")]

    def __str__(self):
        return f"{self.name} ({self.rate * 100:.1f}%)"


# ── Discount ───────────────────────────────────────────────────────────────────


class Discount(models.Model):
    """
    Reusable discount definitions: flat or percentage, optionally limited by usage.
    Applied at the SalesOrder level (cart-wide) or per line item.
    """

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FLAT = "flat", "Flat Amount"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="discounts")
    code = models.CharField(max_length=50, blank=True, db_index=True)
    name = models.CharField(max_length=150)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
    )  # % or flat ₹
    min_order_value = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    max_uses = models.PositiveIntegerField(null=True, blank=True)  # NULL = unlimited
    used_count = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "billing_discount"

    def compute_discount_amount(self, order_total: Decimal) -> Decimal:
        if self.discount_type == self.DiscountType.FLAT:
            return min(self.value, order_total)
        return (self.value / Decimal("100")) * order_total

    def __str__(self):
        return f"{self.name} ({self.shop.name})"


# ── Purchase Order ─────────────────────────────────────────────────────────────


class PurchaseOrder(models.Model):
    """
    Order placed to a Supplier to restock inventory.
    On RECEIVED status, triggers StockMovement(reason=RESTOCK) via signal/service.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SENT = "sent", "Sent to Supplier"
        PARTIAL = "partial", "Partially Received"
        RECEIVED = "received", "Fully Received"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="purchase_orders"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="purchase_orders",
        null=True,
        blank=True,
    )
    po_number = models.CharField(max_length=50, blank=True, db_index=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True
    )

    # Dates
    order_date = models.DateField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)

    # Financials
    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    tax_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    shipping_cost = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    grand_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )

    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_purchaseorder"
        unique_together = [("shop", "po_number")]
        indexes = [
            models.Index(fields=["shop", "status"]),
            models.Index(fields=["shop", "order_date"]),
        ]

    def recalculate_totals(self):
        """Recompute subtotal / tax_total / grand_total from line items."""
        agg = self.items.aggregate(
            sub=Sum("line_total"),
            tax=Sum("tax_amount"),
        )
        self.subtotal = agg["sub"] or Decimal("0.00")
        self.tax_total = agg["tax"] or Decimal("0.00")
        self.grand_total = self.subtotal + self.tax_total + self.shipping_cost
        PurchaseOrder.objects.filter(pk=self.pk).update(
            subtotal=self.subtotal,
            tax_total=self.tax_total,
            grand_total=self.grand_total,
        )

    def __str__(self):
        return f"PO-{self.po_number} ({self.shop.name})"


class PurchaseOrderItem(models.Model):
    """One line per variant on a PurchaseOrder."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="purchase_order_items",
    )
    quantity_ordered = models.PositiveIntegerField()
    quantity_received = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.ForeignKey(
        TaxRate, on_delete=models.SET_NULL, null=True, blank=True
    )
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    line_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )  # unit_cost × quantity_ordered (before tax)
    notes = models.CharField(max_length=300, blank=True)

    class Meta:
        db_table = "billing_purchaseorderitem"

    def save(self, *args, **kwargs):
        self.line_total = self.unit_cost * self.quantity_ordered
        if self.tax_rate:
            self.tax_amount = self.line_total * self.tax_rate.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant} × {self.quantity_ordered} @ {self.unit_cost}"


# ── Sales Order ────────────────────────────────────────────────────────────────


class SalesOrder(models.Model):
    """
    In-store POS transaction or pre-order.
    On COMPLETED status, triggers StockMovement(reason=SALE) via signal/service.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft (cart open)"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed / Paid"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Fully Refunded"

    class Channel(models.TextChoices):
        POS = "pos", "In-Store POS"
        ONLINE = "online", "Online"
        PHONE = "phone", "Phone Order"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="sales_orders"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    order_number = models.CharField(max_length=50, blank=True, db_index=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True
    )
    channel = models.CharField(
        max_length=20, choices=Channel.choices, default=Channel.POS
    )

    # Financials
    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.SET_NULL, null=True, blank=True
    )
    discount_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    tax_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    grand_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    amount_paid = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    change_due = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )

    notes = models.TextField(blank=True)
    served_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_orders_served",
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_salesorder"
        unique_together = [("shop", "order_number")]
        indexes = [
            models.Index(fields=["shop", "status"]),
            models.Index(fields=["shop", "created_at"]),
            models.Index(fields=["customer"]),
        ]

    def recalculate_totals(self):
        agg = self.items.aggregate(
            sub=Sum("line_total"),
            tax=Sum("tax_amount"),
        )
        self.subtotal = agg["sub"] or Decimal("0.00")
        self.tax_total = agg["tax"] or Decimal("0.00")
        disc = (
            self.discount.compute_discount_amount(self.subtotal)
            if self.discount
            else Decimal("0.00")
        )
        self.discount_amount = disc
        self.grand_total = self.subtotal - disc + self.tax_total
        SalesOrder.objects.filter(pk=self.pk).update(
            subtotal=self.subtotal,
            tax_total=self.tax_total,
            discount_amount=self.discount_amount,
            grand_total=self.grand_total,
        )

    def __str__(self):
        return f"SO-{self.order_number} ({self.shop.name})"


class SalesOrderItem(models.Model):
    """One line per variant on a SalesOrder."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.CASCADE, related_name="items"
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name="sales_order_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    # Allows per-line override discounts (e.g. staff discount on one item)
    line_discount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    tax_rate = models.ForeignKey(
        TaxRate, on_delete=models.SET_NULL, null=True, blank=True
    )
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    line_total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    # line_total = (unit_price × quantity) − line_discount, before tax

    class Meta:
        db_table = "billing_salesorderitem"

    def save(self, *args, **kwargs):
        self.line_total = (self.unit_price * self.quantity) - self.line_discount
        if self.tax_rate:
            self.tax_amount = self.line_total * self.tax_rate.rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant} × {self.quantity}"


# ── Invoice ────────────────────────────────────────────────────────────────────


class Invoice(models.Model):
    """
    Formal billing document generated from a completed SalesOrder.
    One SalesOrder → one Invoice (OneToOneField).
    For B2B / GST, generates a tax invoice with GSTIN details.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ISSUED = "issued", "Issued"
        PAID = "paid", "Paid"
        PARTIALLY_PAID = "partial", "Partially Paid"
        OVERDUE = "overdue", "Overdue"
        VOID = "void", "Void"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_order = models.OneToOneField(
        SalesOrder, on_delete=models.PROTECT, related_name="invoice"
    )
    invoice_number = models.CharField(max_length=60, unique=True, db_index=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True
    )
    issued_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    # Snapshot of totals at time of issue (in case order is later edited)
    subtotal_snapshot = models.DecimalField(max_digits=14, decimal_places=2)
    tax_snapshot = models.DecimalField(max_digits=14, decimal_places=2)
    grand_total_snapshot = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )
    balance_due = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal("0.00")
    )

    # Optional PDF blob URL (Cloudflare R2 / S3)
    pdf_url = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_invoice"

    def update_balance(self):
        paid = self.payments.filter(status=Payment.Status.SUCCESS).aggregate(
            s=Sum("amount")
        )["s"] or Decimal("0.00")
        self.amount_paid = paid
        self.balance_due = self.grand_total_snapshot - paid
        if self.balance_due <= 0:
            self.status = self.Status.PAID
        elif paid > 0:
            self.status = self.Status.PARTIALLY_PAID
        Invoice.objects.filter(pk=self.pk).update(
            amount_paid=self.amount_paid,
            balance_due=self.balance_due,
            status=self.status,
        )

    def __str__(self):
        return self.invoice_number


# ── Payment ────────────────────────────────────────────────────────────────────


class Payment(models.Model):
    """
    Individual payment against an Invoice.
    Supports split payments (cash + UPI in one transaction).
    """

    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        UPI = "upi", "UPI"
        CARD = "card", "Card"
        BANK_TRANSFER = "bank", "Bank Transfer"
        CREDIT = "credit", "Store Credit"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )
    method = models.CharField(max_length=20, choices=Method.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    # External gateway reference (Razorpay/Stripe txn ID, UPI ref, etc.)
    reference = models.CharField(max_length=200, blank=True, db_index=True)
    notes = models.CharField(max_length=300, blank=True)
    recorded_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "billing_payment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method} {self.amount} → {self.invoice.invoice_number}"


# ── Return / Refund ────────────────────────────────────────────────────────────


class Return(models.Model):
    """
    Customer return against a completed SalesOrder.
    On APPROVED, triggers StockMovement(reason=RETURN) and a refund Payment row.
    """

    class Reason(models.TextChoices):
        DEFECTIVE = "defective", "Defective"
        WRONG_ITEM = "wrong_item", "Wrong Item"
        NOT_NEEDED = "not_needed", "No Longer Needed"
        SIZE_FIT = "size_fit", "Size / Fit Issue"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        REQUESTED = "requested", "Return Requested"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sales_order = models.ForeignKey(
        SalesOrder, on_delete=models.PROTECT, related_name="returns"
    )
    reason = models.CharField(max_length=30, choices=Reason.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.REQUESTED
    )
    refund_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    refund_payment = models.OneToOneField(
        Payment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="return_record",
    )
    notes = models.TextField(blank=True)
    requested_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="return_requests",
    )
    resolved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="return_resolutions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "billing_return"

    def __str__(self):
        return f"Return #{self.pk} — {self.sales_order}"


class ReturnItem(models.Model):
    """Line items within a Return (which variants are being returned and qty)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    return_record = models.ForeignKey(
        Return, on_delete=models.CASCADE, related_name="items"
    )
    sales_order_item = models.ForeignKey(
        SalesOrderItem, on_delete=models.PROTECT, related_name="return_items"
    )
    quantity = models.PositiveIntegerField()
    restock = models.BooleanField(default=True)  # False = damaged, don't put back

    class Meta:
        db_table = "billing_returnitem"

    def __str__(self):
        return f"{self.sales_order_item.variant} × {self.quantity}"


# ── Bulk Import ────────────────────────────────────────────────────────────────


class BulkImport(models.Model):
    """
    Tracks every CSV bulk-import job: products, stock, or purchase orders.
    One row per upload session; results stored as JSON for the frontend report.
    """

    class ImportType(models.TextChoices):
        PRODUCTS = "products", "Products"
        STOCK_ADJUSTMENT = "stock_adjustment", "Stock Adjustment"
        PURCHASE_ORDER = "purchase_order", "Purchase Order"
        CUSTOMERS = "customers", "Customers"
        PRICE_UPDATE = "price_update", "Price Update"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        DONE = "done", "Done"
        DONE_WITH_ERRORS = "done_errors", "Done with Errors"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="bulk_imports"
    )
    import_type = models.CharField(max_length=30, choices=ImportType.choices)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True
    )

    # Original file (Cloudflare R2 / S3 URL after upload)
    file_url = models.TextField()
    original_filename = models.CharField(max_length=255, blank=True)

    # Counters
    total_rows = models.PositiveIntegerField(default=0)
    rows_succeeded = models.PositiveIntegerField(default=0)
    rows_failed = models.PositiveIntegerField(default=0)

    # Per-row error report: [{"row": 5, "error": "SKU already exists"}]
    error_report = models.JSONField(default=list)

    # Celery task reference for status polling
    task_id = models.CharField(max_length=200, blank=True)

    uploaded_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "billing_bulkimport"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.import_type} import by {self.uploaded_by} — {self.status}"
