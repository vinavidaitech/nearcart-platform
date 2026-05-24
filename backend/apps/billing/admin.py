"""apps/billing/admin.py"""

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action, display

from .models import (
    BulkImport,
    Customer,
    Discount,
    Invoice,
    Payment,
    PurchaseOrder,
    PurchaseOrderItem,
    Return,
    ReturnItem,
    SalesOrder,
    SalesOrderItem,
    Supplier,
    TaxRate,
)


# ── Inlines ────────────────────────────────────────────────────────────────────


class PurchaseOrderItemInline(TabularInline):
    model = PurchaseOrderItem
    extra = 1
    fields = [
        "variant",
        "quantity_ordered",
        "quantity_received",
        "unit_cost",
        "tax_rate",
        "line_total",
    ]
    readonly_fields = ["line_total"]
    show_change_link = True


class SalesOrderItemInline(TabularInline):
    model = SalesOrderItem
    extra = 1
    fields = [
        "variant",
        "quantity",
        "unit_price",
        "line_discount",
        "tax_rate",
        "line_total",
    ]
    readonly_fields = ["line_total"]
    show_change_link = True


class PaymentInline(TabularInline):
    model = Payment
    extra = 0
    fields = ["method", "amount", "status", "reference", "paid_at"]
    readonly_fields = ["paid_at"]


class ReturnItemInline(TabularInline):
    model = ReturnItem
    extra = 1
    fields = ["sales_order_item", "quantity", "restock"]


# ── ModelAdmin registrations ───────────────────────────────────────────────────


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = [
        "name",
        "shop",
        "contact_name",
        "phone",
        "email",
        "payment_terms_days",
        "is_active",
    ]
    list_filter = ["shop", "is_active"]
    search_fields = ["name", "contact_name", "phone", "email", "gstin"]
    list_editable = ["is_active"]


@admin.register(Customer)
class CustomerAdmin(ModelAdmin):
    list_display = [
        "name",
        "shop",
        "phone",
        "email",
        "loyalty_points",
        "credit_balance",
        "created_at",
    ]
    list_filter = ["shop"]
    search_fields = ["name", "phone", "email", "gstin"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(TaxRate)
class TaxRateAdmin(ModelAdmin):
    list_display = ["name", "shop", "rate", "is_default", "is_active"]
    list_filter = ["shop", "is_active"]
    list_editable = ["is_default", "is_active"]


@admin.register(Discount)
class DiscountAdmin(ModelAdmin):
    list_display = [
        "name",
        "shop",
        "code",
        "discount_type",
        "value",
        "used_count",
        "max_uses",
        "is_active",
    ]
    list_filter = ["shop", "discount_type", "is_active"]
    search_fields = ["name", "code"]
    list_editable = ["is_active"]
    readonly_fields = ["used_count"]


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(ModelAdmin):
    list_display = [
        "po_number",
        "shop",
        "supplier",
        "status_badge",
        "order_date",
        "expected_delivery_date",
        "grand_total",
    ]
    list_filter = ["shop", "status", "supplier"]
    search_fields = ["po_number", "supplier__name"]
    readonly_fields = [
        "subtotal",
        "tax_total",
        "grand_total",
        "created_at",
        "updated_at",
    ]
    inlines = [PurchaseOrderItemInline]
    ordering = ["-created_at"]

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "draft": "gray",
            "sent": "blue",
            "partial": "yellow",
            "received": "green",
            "cancelled": "red",
        }
        return obj.status, colours.get(obj.status, "gray")


@admin.register(SalesOrder)
class SalesOrderAdmin(ModelAdmin):
    list_display = [
        "order_number",
        "shop",
        "customer",
        "channel",
        "status_badge",
        "grand_total",
        "amount_paid",
        "created_at",
    ]
    list_filter = ["shop", "status", "channel"]
    search_fields = ["order_number", "customer__name", "customer__phone"]
    readonly_fields = [
        "subtotal",
        "tax_total",
        "discount_amount",
        "grand_total",
        "amount_paid",
        "change_due",
        "created_at",
        "updated_at",
    ]
    inlines = [SalesOrderItemInline]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "draft": "gray",
            "confirmed": "blue",
            "completed": "green",
            "cancelled": "red",
            "refunded": "yellow",
        }
        return obj.status, colours.get(obj.status, "gray")

    actions = ["mark_completed", "mark_cancelled"]

    @action(description="Mark selected as Completed")
    def mark_completed(self, request, queryset):
        from django.utils import timezone

        queryset.filter(status="confirmed").update(
            status="completed", completed_at=timezone.now()
        )

    @action(description="Mark selected as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.exclude(status="completed").update(status="cancelled")


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = [
        "invoice_number",
        "sales_order",
        "status_badge",
        "grand_total_snapshot",
        "amount_paid",
        "balance_due",
        "due_date",
    ]
    list_filter = ["status"]
    search_fields = ["invoice_number", "sales_order__order_number"]
    readonly_fields = [
        "subtotal_snapshot",
        "tax_snapshot",
        "grand_total_snapshot",
        "amount_paid",
        "balance_due",
        "created_at",
        "updated_at",
    ]
    inlines = [PaymentInline]
    ordering = ["-created_at"]

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "draft": "gray",
            "issued": "blue",
            "paid": "green",
            "partial": "yellow",
            "overdue": "red",
            "void": "gray",
        }
        return obj.status, colours.get(obj.status, "gray")


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = [
        "invoice",
        "method",
        "amount",
        "status_badge",
        "reference",
        "paid_at",
    ]
    list_filter = ["method", "status"]
    search_fields = ["reference", "invoice__invoice_number"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "pending": "yellow",
            "success": "green",
            "failed": "red",
            "refunded": "gray",
        }
        return obj.status, colours.get(obj.status, "gray")


@admin.register(Return)
class ReturnAdmin(ModelAdmin):
    list_display = [
        "pk",
        "sales_order",
        "reason",
        "status_badge",
        "refund_amount",
        "created_at",
    ]
    list_filter = ["status", "reason"]
    search_fields = ["sales_order__order_number"]
    readonly_fields = ["created_at", "resolved_at"]
    inlines = [ReturnItemInline]

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "requested": "yellow",
            "approved": "blue",
            "rejected": "red",
            "refunded": "green",
        }
        return obj.status, colours.get(obj.status, "gray")


@admin.register(BulkImport)
class BulkImportAdmin(ModelAdmin):
    list_display = [
        "id",
        "shop",
        "import_type",
        "status_badge",
        "total_rows",
        "rows_succeeded",
        "rows_failed",
        "uploaded_by",
        "created_at",
    ]
    list_filter = ["shop", "import_type", "status"]
    readonly_fields = [
        "total_rows",
        "rows_succeeded",
        "rows_failed",
        "error_report",
        "task_id",
        "created_at",
        "completed_at",
    ]
    ordering = ["-created_at"]

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "pending": "gray",
            "processing": "blue",
            "done": "green",
            "done_errors": "yellow",
            "failed": "red",
        }
        return obj.status, colours.get(obj.status, "gray")
