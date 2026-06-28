from decimal import Decimal
from rest_framework import serializers
from .models import (
    Supplier, Customer, TaxRate, Discount,
    PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
    Invoice, Payment, Return, ReturnItem, BulkImport,
)


# ── Supplier ───────────────────────────────────────────────────────────────────

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_name', 'phone', 'email',
            'address', 'gstin', 'payment_terms_days', 'notes',
            'is_active', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ── Customer ───────────────────────────────────────────────────────────────────

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'user', 'name', 'phone', 'email', 'gstin',
            'address', 'loyalty_points', 'credit_balance',
            'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ── Tax Rate ───────────────────────────────────────────────────────────────────

class TaxRateSerializer(serializers.ModelSerializer):
    rate_percent = serializers.SerializerMethodField()

    class Meta:
        model = TaxRate
        fields = ['id', 'name', 'rate', 'rate_percent', 'is_default', 'is_active']
        read_only_fields = ['id']

    def get_rate_percent(self, obj):
        return float(obj.rate * 100)


# ── Discount ───────────────────────────────────────────────────────────────────

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'id', 'code', 'name', 'discount_type', 'value',
            'min_order_value', 'max_uses', 'used_count',
            'valid_from', 'valid_until', 'is_active',
        ]
        read_only_fields = ['id', 'used_count']


# ── Purchase Order ─────────────────────────────────────────────────────────────

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrderItem
        fields = [
            'id', 'variant', 'variant_name', 'product_name',
            'quantity_ordered', 'quantity_received',
            'unit_cost', 'tax_rate', 'tax_amount', 'line_total', 'notes',
        ]
        read_only_fields = ['id', 'tax_amount', 'line_total']

    def get_variant_name(self, obj):
        return str(obj.variant)

    def get_product_name(self, obj):
        return obj.variant.product.name


class PurchaseOrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = [
            'variant', 'quantity_ordered', 'quantity_received',
            'unit_cost', 'tax_rate', 'notes',
        ]


class PurchaseOrderListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True, default=None)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'status', 'supplier_name',
            'order_date', 'expected_delivery_date', 'received_at',
            'subtotal', 'tax_total', 'shipping_cost', 'grand_total',
            'item_count', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_item_count(self, obj):
        return obj.items.count()


class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True, default=None)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'po_number', 'status', 'supplier', 'supplier_name',
            'order_date', 'expected_delivery_date', 'received_at',
            'subtotal', 'tax_total', 'shipping_cost', 'grand_total',
            'notes', 'created_by', 'created_by_name', 'items',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'subtotal', 'tax_total', 'grand_total',
            'created_by', 'created_at', 'updated_at',
        ]

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None


class PurchaseOrderWriteSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemWriteSerializer(many=True, required=False)

    class Meta:
        model = PurchaseOrder
        fields = [
            'supplier', 'po_number', 'status',
            'order_date', 'expected_delivery_date',
            'shipping_cost', 'notes', 'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        shop = self.context['shop']
        po = PurchaseOrder.objects.create(
            shop=shop, created_by=self.context['request'].user, **validated_data
        )
        for item in items_data:
            PurchaseOrderItem.objects.create(purchase_order=po, **item)
        po.recalculate_totals()
        return po

    def update(self, instance, validated_data):
        validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.recalculate_totals()
        return instance


# ── Sales Order ────────────────────────────────────────────────────────────────

class SalesOrderItemSerializer(serializers.ModelSerializer):
    variant_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrderItem
        fields = [
            'id', 'variant', 'variant_name', 'product_name',
            'quantity', 'unit_price', 'line_discount',
            'tax_rate', 'tax_amount', 'line_total',
        ]
        read_only_fields = ['id', 'tax_amount', 'line_total']

    def get_variant_name(self, obj):
        return str(obj.variant)

    def get_product_name(self, obj):
        return obj.variant.product.name


class SalesOrderItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ['variant', 'quantity', 'unit_price', 'line_discount', 'tax_rate']


class SalesOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True, default=None)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True, default=None)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'status', 'channel',
            'customer_name', 'customer_phone',
            'subtotal', 'discount_amount', 'tax_total', 'grand_total',
            'payment_method', 'item_count',
            'completed_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_item_count(self, obj):
        return obj.items.count()


class SalesOrderDetailSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    served_by_name = serializers.SerializerMethodField()
    discount_code = serializers.CharField(source='discount.code', read_only=True, default=None)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'status', 'channel',
            'customer', 'served_by', 'served_by_name',
            'subtotal', 'discount', 'discount_code', 'discount_amount',
            'tax_total', 'grand_total', 'amount_paid', 'change_due',
            'payment_method', 'notes', 'items',
            'completed_at', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'subtotal', 'discount_amount', 'tax_total', 'grand_total',
            'served_by', 'created_at', 'updated_at',
        ]

    def get_served_by_name(self, obj):
        return obj.served_by.get_full_name() if obj.served_by else None


class SalesOrderWriteSerializer(serializers.ModelSerializer):
    """Create/update a sales order with inline items."""
    items = SalesOrderItemWriteSerializer(many=True, required=False)

    class Meta:
        model = SalesOrder
        fields = [
            'customer', 'channel', 'status', 'discount',
            'payment_method', 'amount_paid', 'change_due', 'notes',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        shop = self.context['shop']
        order = SalesOrder.objects.create(
            shop=shop, served_by=self.context['request'].user, **validated_data
        )
        for item in items_data:
            SalesOrderItem.objects.create(sales_order=order, **item)
        order.recalculate_totals()
        return order

    def update(self, instance, validated_data):
        validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.recalculate_totals()
        return instance


# ── Invoice ────────────────────────────────────────────────────────────────────

class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_phone = serializers.SerializerMethodField()
    order_number = serializers.CharField(source='sales_order.order_number', read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'status', 'order_number',
            'customer_name', 'customer_phone',
            'subtotal_snapshot', 'tax_snapshot', 'grand_total_snapshot',
            'amount_paid', 'balance_due',
            'issued_at', 'due_date', 'pdf_url', 'notes',
            'items', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'amount_paid', 'balance_due', 'created_at', 'updated_at',
        ]

    def get_customer_name(self, obj):
        return obj.sales_order.customer.name if obj.sales_order.customer else 'Walk-in'

    def get_customer_phone(self, obj):
        return obj.sales_order.customer.phone if obj.sales_order.customer else ''

    def get_items(self, obj):
        return SalesOrderItemSerializer(obj.sales_order.items.all(), many=True).data


# ── Payment ────────────────────────────────────────────────────────────────────

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'method', 'status', 'amount',
            'reference', 'notes', 'recorded_by', 'paid_at', 'created_at',
        ]
        read_only_fields = ['id', 'recorded_by', 'created_at']


# ── Return ─────────────────────────────────────────────────────────────────────

class ReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = ['id', 'sales_order_item', 'quantity', 'restock']
        read_only_fields = ['id']


class ReturnSerializer(serializers.ModelSerializer):
    items = ReturnItemSerializer(many=True, read_only=True)

    class Meta:
        model = Return
        fields = [
            'id', 'sales_order', 'reason', 'status',
            'refund_amount', 'refund_payment', 'notes',
            'requested_by', 'resolved_by',
            'created_at', 'resolved_at', 'items',
        ]
        read_only_fields = ['id', 'requested_by', 'resolved_by', 'created_at', 'resolved_at']


# ── BulkImport ────────────────────────────────────────────────────────────────

class BulkImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkImport
        fields = [
            'id', 'import_type', 'status', 'file_url', 'original_filename',
            'total_rows', 'rows_succeeded', 'rows_failed',
            'error_report', 'task_id', 'uploaded_by',
            'created_at', 'completed_at',
        ]
        read_only_fields = [
            'id', 'status', 'total_rows', 'rows_succeeded', 'rows_failed',
            'error_report', 'task_id', 'uploaded_by', 'created_at', 'completed_at',
        ]
