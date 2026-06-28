from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.inventory.models import ProductVariant, StockMovement
from apps.shops.models import Shop
from .models import (
    Supplier, Customer, TaxRate, Discount,
    PurchaseOrder, PurchaseOrderItem,
    SalesOrder, SalesOrderItem,
    Invoice, Payment, Return, ReturnItem, BulkImport,
)
from .serializers import (
    SupplierSerializer, CustomerSerializer, TaxRateSerializer,
    DiscountSerializer, PurchaseOrderListSerializer,
    PurchaseOrderDetailSerializer, PurchaseOrderWriteSerializer,
    SalesOrderListSerializer, SalesOrderDetailSerializer,
    SalesOrderWriteSerializer, InvoiceSerializer,
    PaymentSerializer, ReturnSerializer, ReturnItemSerializer,
    BulkImportSerializer,
)


def get_shop_or_404(request):
    shop_id = request.headers.get('X-Shop-ID') or request.query_params.get('shop_id')
    if not shop_id:
        return None, Response(
            {'detail': 'X-Shop-ID header or shop_id query param required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        shop = Shop.objects.get(id=shop_id, owner=request.user)
        return shop, None
    except Shop.DoesNotExist:
        return None, Response(
            {'detail': 'Shop not found or access denied.'},
            status=status.HTTP_404_NOT_FOUND,
        )


class ShopScopedMixin:
    def get_shop(self):
        if not hasattr(self, '_shop'):
            shop, error = get_shop_or_404(self.request)
            if error:
                raise PermissionError('shop_required')
            self._shop = shop
        return self._shop


# ── Supplier ───────────────────────────────────────────────────────────────────

class SupplierViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /billing/suppliers/       — list
    POST   /billing/suppliers/       — create
    GET    /billing/suppliers/{id}/  — detail
    PUT    /billing/suppliers/{id}/  — update
    DELETE /billing/suppliers/{id}/  — soft delete
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer

    def get_queryset(self):
        shop = self.get_shop()
        qs = Supplier.objects.filter(shop=shop)
        active = self.request.query_params.get('is_active')
        if active is not None:
            qs = qs.filter(is_active=active.lower() == 'true')
        else:
            qs = qs.filter(is_active=True)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs.order_by('name')

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())

    def destroy(self, request, *args, **kwargs):
        supplier = self.get_object()
        supplier.is_active = False
        supplier.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Customer ───────────────────────────────────────────────────────────────────

class CustomerViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /billing/customers/       — list (search by name/phone)
    POST   /billing/customers/       — create walk-in or registered customer
    GET    /billing/customers/{id}/  — detail with order history
    PUT    /billing/customers/{id}/  — update
    GET    /billing/customers/{id}/orders/ — orders for this customer
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        shop = self.get_shop()
        qs = Customer.objects.filter(shop=shop)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(phone__icontains=search)
        return qs.order_by('name')

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())

    @action(detail=True, methods=['get'], url_path='orders')
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.orders.order_by('-created_at')[:50]
        return Response(SalesOrderListSerializer(orders, many=True).data)


# ── Tax Rate ───────────────────────────────────────────────────────────────────

class TaxRateViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """GET/POST/PUT/DELETE /billing/tax-rates/"""
    permission_classes = [IsAuthenticated]
    serializer_class = TaxRateSerializer

    def get_queryset(self):
        return TaxRate.objects.filter(shop=self.get_shop(), is_active=True)

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())


# ── Discount ───────────────────────────────────────────────────────────────────

class DiscountViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET  /billing/discounts/              — list active discounts
    POST /billing/discounts/validate/     — validate a discount code
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DiscountSerializer

    def get_queryset(self):
        shop = self.get_shop()
        return Discount.objects.filter(shop=shop, is_active=True)

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())

    @action(detail=False, methods=['post'], url_path='validate')
    def validate_code(self, request):
        code = request.data.get('code', '').strip()
        order_total = request.data.get('order_total', 0)
        try:
            discount = Discount.objects.get(
                shop=self.get_shop(), code=code, is_active=True
            )
        except Discount.DoesNotExist:
            return Response({'valid': False, 'detail': 'Invalid discount code.'})

        now = timezone.now()
        if discount.valid_from and discount.valid_from > now:
            return Response({'valid': False, 'detail': 'Discount not yet active.'})
        if discount.valid_until and discount.valid_until < now:
            return Response({'valid': False, 'detail': 'Discount has expired.'})
        if discount.max_uses and discount.used_count >= discount.max_uses:
            return Response({'valid': False, 'detail': 'Discount usage limit reached.'})

        from decimal import Decimal
        amount = discount.compute_discount_amount(Decimal(str(order_total)))
        return Response({
            'valid': True,
            'discount_id': str(discount.id),
            'discount_amount': float(amount),
            'discount_type': discount.discount_type,
            'value': float(discount.value),
        })


# ── Purchase Orders ────────────────────────────────────────────────────────────

class PurchaseOrderViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /billing/purchase-orders/              — list
    POST   /billing/purchase-orders/              — create
    GET    /billing/purchase-orders/{id}/         — detail with items
    PATCH  /billing/purchase-orders/{id}/         — update status / details
    POST   /billing/purchase-orders/{id}/receive/ — mark as received, update stock
    POST   /billing/purchase-orders/{id}/items/   — add item to existing PO
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop = self.get_shop()
        qs = PurchaseOrder.objects.filter(shop=shop).select_related(
            'supplier', 'created_by'
        ).prefetch_related('items__variant__product')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        supplier = self.request.query_params.get('supplier')
        if supplier:
            qs = qs.filter(supplier_id=supplier)

        return qs.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return PurchaseOrderListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return PurchaseOrderWriteSerializer
        return PurchaseOrderDetailSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        try:
            ctx['shop'] = self.get_shop()
        except Exception:
            pass
        return ctx

    @action(detail=True, methods=['post'], url_path='receive')
    def receive(self, request, pk=None):
        """
        Mark PO as received. For each item, create a StockMovement(RESTOCK)
        and bump the variant's stock_count.
        """
        po = self.get_object()
        if po.status == PurchaseOrder.Status.RECEIVED:
            return Response({'detail': 'Already received.'}, status=status.HTTP_400_BAD_REQUEST)
        if po.status == PurchaseOrder.Status.CANCELLED:
            return Response({'detail': 'Cannot receive a cancelled PO.'}, status=status.HTTP_400_BAD_REQUEST)

        for item in po.items.select_related('variant__product').all():
            qty_to_receive = item.quantity_ordered - item.quantity_received
            if qty_to_receive <= 0:
                continue
            variant = item.variant
            variant.stock_count += qty_to_receive
            variant.save(update_fields=['stock_count'])
            item.quantity_received = item.quantity_ordered
            item.save(update_fields=['quantity_received'])

            StockMovement.objects.create(
                variant=variant,
                change_qty=qty_to_receive,
                reason=StockMovement.Reason.RESTOCK,
                reference=po.po_number or str(po.id),
                performed_by=request.user,
            )
            variant.product.recalculate_stock()

        po.status = PurchaseOrder.Status.RECEIVED
        po.received_at = timezone.now()
        po.save(update_fields=['status', 'received_at'])

        return Response(PurchaseOrderDetailSerializer(po).data)

    @action(detail=True, methods=['post', 'get'], url_path='items')
    def items(self, request, pk=None):
        po = self.get_object()
        if request.method == 'GET':
            from .serializers import PurchaseOrderItemSerializer
            return Response(PurchaseOrderItemSerializer(po.items.all(), many=True).data)

        from .serializers import PurchaseOrderItemWriteSerializer
        serializer = PurchaseOrderItemWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(purchase_order=po)
        po.recalculate_totals()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ── Sales Orders ───────────────────────────────────────────────────────────────

class SalesOrderViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /billing/sales-orders/                 — list (filterable by status, customer)
    POST   /billing/sales-orders/                 — create (POS checkout)
    GET    /billing/sales-orders/{id}/            — detail
    PATCH  /billing/sales-orders/{id}/            — update
    POST   /billing/sales-orders/{id}/complete/   — mark completed, deduct stock, gen invoice
    POST   /billing/sales-orders/{id}/cancel/     — cancel order
    GET    /billing/sales-orders/summary/         — today's revenue summary
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop = self.get_shop()
        qs = SalesOrder.objects.filter(shop=shop).select_related(
            'customer', 'discount', 'served_by'
        ).prefetch_related('items__variant__product')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        customer = self.request.query_params.get('customer')
        if customer:
            qs = qs.filter(customer_id=customer)

        channel = self.request.query_params.get('channel')
        if channel:
            qs = qs.filter(channel=channel)

        date_from = self.request.query_params.get('date_from')
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)

        date_to = self.request.query_params.get('date_to')
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        return qs.order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return SalesOrderListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return SalesOrderWriteSerializer
        return SalesOrderDetailSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        try:
            ctx['shop'] = self.get_shop()
        except Exception:
            pass
        return ctx

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """
        1. Mark order COMPLETED
        2. Deduct stock for each line item (StockMovement SALE)
        3. Generate Invoice
        """
        order = self.get_object()
        if order.status == SalesOrder.Status.COMPLETED:
            return Response({'detail': 'Already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == SalesOrder.Status.CANCELLED:
            return Response({'detail': 'Cannot complete a cancelled order.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct stock
        for item in order.items.select_related('variant__product').all():
            variant = item.variant
            variant.stock_count = max(0, variant.stock_count - item.quantity)
            variant.save(update_fields=['stock_count'])
            StockMovement.objects.create(
                variant=variant,
                change_qty=-item.quantity,
                reason=StockMovement.Reason.SALE,
                reference=order.order_number or str(order.id),
                performed_by=request.user,
            )
            variant.product.recalculate_stock()

        order.status = SalesOrder.Status.COMPLETED
        order.completed_at = timezone.now()
        order.save(update_fields=['status', 'completed_at'])

        # Generate Invoice if not already exists
        if not hasattr(order, 'invoice'):
            import uuid as _uuid
            Invoice.objects.create(
                sales_order=order,
                invoice_number=f"INV-{str(order.id)[:8].upper()}",
                status=Invoice.Status.PAID if order.amount_paid >= order.grand_total else Invoice.Status.ISSUED,
                issued_at=timezone.now(),
                subtotal_snapshot=order.subtotal,
                tax_snapshot=order.tax_total,
                grand_total_snapshot=order.grand_total,
                amount_paid=order.amount_paid,
                balance_due=max(order.grand_total - order.amount_paid, 0),
            )

        return Response(SalesOrderDetailSerializer(order).data)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status in (SalesOrder.Status.COMPLETED, SalesOrder.Status.CANCELLED):
            return Response(
                {'detail': f'Cannot cancel an order with status: {order.status}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        order.status = SalesOrder.Status.CANCELLED
        order.save(update_fields=['status'])
        return Response({'detail': 'Order cancelled.'})

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        """Today's sales summary for the dashboard."""
        from django.db.models import Sum, Count
        from django.utils.timezone import localdate
        shop = self.get_shop()
        today = localdate()
        qs = SalesOrder.objects.filter(
            shop=shop, status=SalesOrder.Status.COMPLETED,
            completed_at__date=today,
        )
        agg = qs.aggregate(
            total_revenue=Sum('grand_total'),
            order_count=Count('id'),
            total_tax=Sum('tax_total'),
        )
        return Response({
            'date': str(today),
            'total_revenue': float(agg['total_revenue'] or 0),
            'order_count': agg['order_count'] or 0,
            'total_tax': float(agg['total_tax'] or 0),
        })


# ── Invoice ────────────────────────────────────────────────────────────────────

class InvoiceViewSet(ShopScopedMixin, viewsets.ReadOnlyModelViewSet):
    """
    GET /billing/invoices/       — list all invoices for shop
    GET /billing/invoices/{id}/  — invoice detail
    """
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        shop = self.get_shop()
        qs = Invoice.objects.filter(
            sales_order__shop=shop
        ).select_related('sales_order__customer').prefetch_related('sales_order__items__variant__product')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs.order_by('-created_at')


# ── Payment ────────────────────────────────────────────────────────────────────

class PaymentViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET  /billing/payments/              — list payments
    POST /billing/payments/              — record a payment
    GET  /billing/payments/{id}/         — detail
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        shop = self.get_shop()
        qs = Payment.objects.filter(
            invoice__sales_order__shop=shop
        ).select_related('invoice', 'recorded_by')

        invoice_id = self.request.query_params.get('invoice')
        if invoice_id:
            qs = qs.filter(invoice_id=invoice_id)

        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        payment = serializer.save(recorded_by=self.request.user)
        payment.invoice.update_balance()


# ── Returns ────────────────────────────────────────────────────────────────────

class ReturnViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /billing/returns/              — list returns
    POST   /billing/returns/              — create return request
    PATCH  /billing/returns/{id}/         — update (approve/reject)
    POST   /billing/returns/{id}/approve/ — approve + restock + refund
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReturnSerializer

    def get_queryset(self):
        shop = self.get_shop()
        return Return.objects.filter(
            sales_order__shop=shop
        ).select_related('sales_order', 'requested_by', 'resolved_by').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        ret = self.get_object()
        if ret.status != Return.Status.REQUESTED:
            return Response({'detail': 'Return is not in REQUESTED state.'}, status=status.HTTP_400_BAD_REQUEST)

        # Restock items
        for return_item in ret.items.select_related('sales_order_item__variant__product').all():
            if return_item.restock:
                variant = return_item.sales_order_item.variant
                variant.stock_count += return_item.quantity
                variant.save(update_fields=['stock_count'])
                StockMovement.objects.create(
                    variant=variant,
                    change_qty=return_item.quantity,
                    reason=StockMovement.Reason.RETURN,
                    reference=str(ret.id),
                    performed_by=request.user,
                )
                variant.product.recalculate_stock()

        ret.status = Return.Status.APPROVED
        ret.resolved_by = request.user
        ret.resolved_at = timezone.now()
        ret.save(update_fields=['status', 'resolved_by', 'resolved_at'])
        return Response(ReturnSerializer(ret).data)


