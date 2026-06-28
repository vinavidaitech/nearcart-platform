from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.shops.models import Shop
from .models import (
    LocationNode, ProductCategory, Brand, Product,
    ProductVariant, ProductImage, StockMovement,
)
from .serializers import (
    LocationNodeSerializer, ProductCategorySerializer, BrandSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductWriteSerializer,
    ProductVariantSerializer, ProductVariantWriteSerializer,
    ProductImageSerializer, StockMovementSerializer, StockAdjustSerializer,
    AttributeSchemaSerializer,
)


def get_shop_or_404(request):
    """Return the shop scoped to the current request (via header or query param)."""
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
    """Mixin that injects shop into every action."""

    def get_shop(self):
        if not hasattr(self, '_shop'):
            shop, error = get_shop_or_404(self.request)
            if error:
                raise PermissionError('shop_required')
            self._shop = shop
        return self._shop

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionError as e:
            if str(e) == 'shop_required':
                return Response(
                    {'detail': 'X-Shop-ID header or shop_id query param required.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            raise


# ── Location Nodes ─────────────────────────────────────────────────────────────

class LocationNodeViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET  /inventory/locations/          — tree of all active nodes
    POST /inventory/locations/          — create root or child node
    GET  /inventory/locations/{id}/     — single node
    PUT  /inventory/locations/{id}/     — update
    DEL  /inventory/locations/{id}/     — delete
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LocationNodeSerializer

    def get_queryset(self):
        shop = self.get_shop()
        qs = LocationNode.objects.filter(shop=shop, is_active=True)
        parent = self.request.query_params.get('parent')
        if parent == 'root':
            qs = qs.filter(parent__isnull=True)
        elif parent:
            qs = qs.filter(parent_id=parent)
        return qs.order_by('sort_order', 'name')

    def perform_create(self, serializer):
        serializer.save(shop=self.get_shop())


# ── Product Categories ─────────────────────────────────────────────────────────

class ProductCategoryViewSet(viewsets.ModelViewSet):

    """
    GET    /inventory/categories/       — all active categories
    POST   /inventory/categories/       — create category
    PATCH  /inventory/categories/{id}/  — update category
    DELETE /inventory/categories/{id}/  — delete category
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.filter(is_active=True).order_by('name')


# ── Brands ────────────────────────────────────────────────────────────────────

class BrandViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for brands (global, not shop-scoped).
    GET  /inventory/brands/
    POST /inventory/brands/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer
    queryset = Brand.objects.all().order_by('name')


# ── Products ──────────────────────────────────────────────────────────────────

class ProductViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /inventory/products/                  — list (paginated, filterable)
    POST   /inventory/products/                  — create
    GET    /inventory/products/{id}/             — detail
    PUT    /inventory/products/{id}/             — full update
    PATCH  /inventory/products/{id}/             — partial update
    DELETE /inventory/products/{id}/             — soft-delete (is_active=False)

    POST   /inventory/products/{id}/adjust-stock/ — manual stock adjustment
    GET    /inventory/products/{id}/movements/    — stock movement history
    POST   /inventory/products/{id}/images/       — upload image metadata
    GET    /inventory/products/low-stock/         — products at or below threshold
    GET    /inventory/products/out-of-stock/      — products with 0 stock
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop = self.get_shop()
        qs = Product.objects.filter(shop=shop).select_related(
            'category', 'brand', 'primary_location_node',
        ).prefetch_related('images', 'variants')

        # Filters
        active = self.request.query_params.get('is_active')
        if active is not None:
            qs = qs.filter(is_active=active.lower() == 'true')
        else:
            qs = qs.filter(is_active=True)

        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category_id=category)

        brand = self.request.query_params.get('brand')
        if brand:
            qs = qs.filter(brand_id=brand)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(sku__icontains=search)

        stock_status = self.request.query_params.get('stock_status')
        if stock_status == 'out':
            qs = qs.filter(total_stock=0)
        elif stock_status == 'low':
            from django.db.models import F
            qs = qs.filter(total_stock__lte=F('low_stock_threshold'), total_stock__gt=0)

        return qs.order_by('name')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ProductWriteSerializer
        return ProductDetailSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        try:
            ctx['shop'] = self.get_shop()
        except Exception:
            pass
        return ctx

    def destroy(self, request, *args, **kwargs):
        """Soft-delete: set is_active=False instead of hard delete."""
        product = self.get_object()
        product.is_active = False
        product.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='adjust-stock')
    def adjust_stock(self, request, pk=None):
        product = self.get_object()
        serializer = StockAdjustSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        try:
            variant = product.variants.get(id=d['variant_id'], is_active=True)
        except ProductVariant.DoesNotExist:
            return Response({'detail': 'Variant not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_count = max(0, variant.stock_count + d['change_qty'])
        variant.stock_count = new_count
        variant.save(update_fields=['stock_count'])

        StockMovement.objects.create(
            variant=variant,
            change_qty=d['change_qty'],
            reason=d['reason'],
            reference=d.get('reference', ''),
            performed_by=request.user,
        )

        product.recalculate_stock()
        return Response({'stock_count': new_count, 'total_stock': product.total_stock})

    @action(detail=True, methods=['get'], url_path='movements')
    def movements(self, request, pk=None):
        product = self.get_object()
        variant_ids = product.variants.values_list('id', flat=True)
        movements = StockMovement.objects.filter(
            variant_id__in=variant_ids
        ).select_related('performed_by', 'variant').order_by('-created_at')[:100]
        return Response(StockMovementSerializer(movements, many=True).data)

    @action(detail=True, methods=['post', 'get'], url_path='images')
    def images(self, request, pk=None):
        product = self.get_object()
        if request.method == 'GET':
            return Response(ProductImageSerializer(product.images.all(), many=True).data)
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        from django.db.models import F
        shop = self.get_shop()
        qs = Product.objects.filter(
            shop=shop, is_active=True,
            total_stock__lte=F('low_stock_threshold'),
            total_stock__gt=0,
        ).order_by('total_stock')
        return Response(ProductListSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='out-of-stock')
    def out_of_stock(self, request):
        shop = self.get_shop()
        qs = Product.objects.filter(shop=shop, is_active=True, total_stock=0).order_by('name')
        return Response(ProductListSerializer(qs, many=True).data)


# ── Product Variants ──────────────────────────────────────────────────────────

class ProductVariantViewSet(ShopScopedMixin, viewsets.ModelViewSet):
    """
    GET    /inventory/variants/?product={id}  — list variants for a product
    POST   /inventory/variants/               — create variant
    PATCH  /inventory/variants/{id}/          — update variant
    DELETE /inventory/variants/{id}/          — soft-delete
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop = self.get_shop()
        qs = ProductVariant.objects.filter(
            product__shop=shop, is_active=True
        ).select_related('product')
        product_id = self.request.query_params.get('product')
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ProductVariantWriteSerializer
        return ProductVariantSerializer

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        shop = self.get_shop()
        product = Product.objects.get(id=product_id, shop=shop)
        instance = serializer.save(product=product)
        instance.product.recalculate_stock()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.product.recalculate_stock()

    def destroy(self, request, *args, **kwargs):
        variant = self.get_object()
        variant.is_active = False
        variant.save(update_fields=['is_active'])
        variant.product.recalculate_stock()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Stock Movements ───────────────────────────────────────────────────────────

class StockMovementViewSet(ShopScopedMixin, viewsets.ReadOnlyModelViewSet):
    """
    GET /inventory/movements/              — all movements for the shop
    GET /inventory/movements/?variant={id} — filter by variant
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StockMovementSerializer

    def get_queryset(self):
        shop = self.get_shop()
        qs = StockMovement.objects.filter(
            variant__product__shop=shop
        ).select_related('variant__product', 'performed_by').order_by('-created_at')

        variant_id = self.request.query_params.get('variant')
        if variant_id:
            qs = qs.filter(variant_id=variant_id)

        reason = self.request.query_params.get('reason')
        if reason:
            qs = qs.filter(reason=reason)

        return qs[:200]
