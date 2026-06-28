from rest_framework import serializers
from .models import (
    LocationNode, ProductCategory, Brand, AttributeSchema,
    Product, ProductVariant, ProductImage, PriceHistory, StockMovement,
)


class LocationNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = LocationNode
        fields = [
            'id', 'parent', 'level', 'name', 'code', 'path',
            'sort_order', 'is_active', 'children',
        ]
        read_only_fields = ['id', 'path']

    def get_children(self, obj):
        return LocationNodeSerializer(
            obj.children.filter(is_active=True).order_by('sort_order'), many=True
        ).data


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'parent', 'shop_category', 'name', 'slug', 'is_active']
        read_only_fields = ['id']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo_url']
        read_only_fields = ['id']


class AttributeSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeSchema
        fields = [
            'id', 'shop_category', 'key', 'label', 'data_type',
            'is_variant', 'is_filterable', 'sort_order',
        ]
        read_only_fields = ['id']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'alt_text', 'sort_order', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductVariantSerializer(serializers.ModelSerializer):
    effective_price = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = [
            'id', 'product', 'variant_attributes', 'sku_suffix',
            'stock_count', 'price_override', 'effective_price',
            'location_node_override', 'bin_label_override', 'is_active',
        ]
        read_only_fields = ['id', 'effective_price']


class ProductVariantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'variant_attributes', 'sku_suffix', 'stock_count',
            'price_override', 'location_node_override', 'bin_label_override', 'is_active',
        ]


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


class StockMovementSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.SerializerMethodField()
    variant_display = serializers.SerializerMethodField()

    class Meta:
        model = StockMovement
        fields = [
            'id', 'variant', 'variant_display', 'change_qty', 'reason',
            'reference', 'performed_by', 'performed_by_name', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_performed_by_name(self, obj):
        return obj.performed_by.get_full_name() if obj.performed_by else None

    def get_variant_display(self, obj):
        return str(obj.variant)


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, default=None)
    primary_image = serializers.SerializerMethodField()
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'sku', 'barcode', 'name', 'base_price', 'compare_at_price',
            'total_stock', 'low_stock_threshold', 'is_active',
            'category_name', 'brand_name', 'primary_image', 'stock_status',
            'floor_label', 'aisle_label', 'shelf_label', 'bin_label',
            'attributes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'total_stock', 'created_at', 'updated_at']

    def get_primary_image(self, obj):
        img = obj.images.filter(is_primary=True).first() or obj.images.first()
        return img.url if img else None

    def get_stock_status(self, obj):
        if obj.total_stock == 0:
            return 'out'
        if obj.total_stock <= obj.low_stock_threshold:
            return 'low'
        return 'ok'


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer with nested variants, images, price history."""
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True, source='price_history')
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, default=None)
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'shop', 'sku', 'barcode', 'name', 'description',
            'base_price', 'compare_at_price', 'attributes',
            'total_stock', 'low_stock_threshold', 'is_active',
            'category', 'category_name', 'brand', 'brand_name',
            'floor_label', 'aisle_label', 'shelf_label', 'bin_label',
            'location_notes', 'primary_location_node', 'location_updated_at',
            'variants', 'images', 'price_history', 'stock_status',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'shop', 'total_stock', 'created_at', 'updated_at',
        ]

    def get_stock_status(self, obj):
        if obj.total_stock == 0:
            return 'out'
        if obj.total_stock <= obj.low_stock_threshold:
            return 'low'
        return 'ok'


class ProductWriteSerializer(serializers.ModelSerializer):
    """Used for create / update — shop injected from request context."""
    variants = ProductVariantWriteSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'sku', 'barcode', 'name', 'description', 'base_price',
            'compare_at_price', 'category', 'brand', 'attributes',
            'low_stock_threshold', 'is_active',
            'floor_label', 'aisle_label', 'shelf_label', 'bin_label',
            'location_notes', 'primary_location_node',
            'variants',
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop('variants', [])
        shop = self.context['shop']
        product = Product.objects.create(shop=shop, **validated_data)
        for v in variants_data:
            ProductVariant.objects.create(product=product, **v)
        product.recalculate_stock()
        return product

    def update(self, instance, validated_data):
        validated_data.pop('variants', None)  # variants managed separately
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class StockAdjustSerializer(serializers.Serializer):
    """Body for POST /products/{id}/adjust-stock/"""
    variant_id = serializers.UUIDField()
    change_qty = serializers.IntegerField()
    reason = serializers.ChoiceField(choices=StockMovement.Reason.choices)
    reference = serializers.CharField(required=False, allow_blank=True, default='')
    note = serializers.CharField(required=False, allow_blank=True, default='')
