# from apps.inventory.models import (
#     AttributeSchema,
#     Brand,
#     LocationNode,
#     PriceHistory,
#     Product,
#     ProductCategory,
#     ProductImage,
#     ProductVariant,
#     StockMovement,
# )
# from django.contrib import admin

# Register your models here.
# admin.site.register(Brand)
# admin.site.register(Product)
# admin.site.register(ProductImage)
# admin.site.register(ProductVariant)
# admin.site.register(ProductCategory)
# admin.site.register(LocationNode)
# admin.site.register(AttributeSchema)
# admin.site.register(PriceHistory)
# admin.site.register(StockMovement)


"""apps/inventory/admin.py"""

from django.contrib import admin
from django.db.models import F
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.decorators import display

from .models import (
    AttributeSchema,
    Brand,
    LocationNode,
    PriceHistory,
    Product,
    ProductCategory,
    ProductImage,
    ProductVariant,
    StockMovement,
)


class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 1
    fields = [
        "variant_attributes",
        "sku_suffix",
        "stock_count",
        "price_override",
        "is_active",
    ]


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 0
    fields = ["url", "alt_text", "sort_order", "is_primary"]


class PriceHistoryInline(TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ["price", "recorded_at"]
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        "name",
        "shop",
        "category",
        "brand",
        "base_price",
        "stock_badge",
        "is_active",
        "updated_at",
    ]
    list_filter = ["shop", "category", "brand", "is_active"]
    search_fields = ["name", "sku", "barcode"]
    readonly_fields = ["total_stock", "created_at", "updated_at", "location_updated_at"]
    list_editable = ["is_active"]
    inlines = [ProductVariantInline, ProductImageInline, PriceHistoryInline]
    ordering = ["-updated_at"]
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Core",
            {
                "fields": (
                    "shop",
                    "category",
                    "brand",
                    "name",
                    "description",
                    "sku",
                    "barcode",
                )
            },
        ),
        ("Pricing", {"fields": ("base_price", "compare_at_price")}),
        ("Stock", {"fields": ("total_stock", "low_stock_threshold")}),
        (
            "Location",
            {
                "fields": (
                    "floor_label",
                    "aisle_label",
                    "shelf_label",
                    "primary_location_node",
                    "bin_label",
                    "location_notes",
                    "location_updated_at",
                )
            },
        ),
        ("Attributes", {"fields": ("attributes",)}),
        ("Status", {"fields": ("is_active", "created_at", "updated_at")}),
    )

    @display(description="Stock", label=True)
    def stock_badge(self, obj):
        if obj.total_stock == 0:
            return f"{obj.total_stock}", "red"
        if obj.total_stock <= obj.low_stock_threshold:
            return f"{obj.total_stock} ⚠", "yellow"
        return f"{obj.total_stock}", "green"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("shop", "category", "brand")


@admin.register(ProductVariant)
class ProductVariantAdmin(ModelAdmin):
    list_display = [
        "product",
        "variant_attributes",
        "sku_suffix",
        "stock_count",
        "effective_price",
        "is_active",
    ]
    list_filter = ["is_active", "product__shop"]
    search_fields = ["product__name", "sku_suffix"]
    readonly_fields = ["effective_price"]


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ["name", "slug", "parent", "shop_category", "is_active"]
    list_filter = ["is_active", "shop_category"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(LocationNode)
class LocationNodeAdmin(ModelAdmin):
    list_display = ["path", "shop", "level", "code", "is_active", "sort_order"]
    list_filter = ["shop", "level", "is_active"]
    search_fields = ["name", "code", "path"]
    ordering = ["shop", "path"]


@admin.register(StockMovement)
class StockMovementAdmin(ModelAdmin):
    list_display = [
        "variant",
        "change_qty",
        "reason",
        "reference",
        "performed_by",
        "created_at",
    ]
    list_filter = ["reason", "created_at"]
    search_fields = ["variant__product__name", "reference"]
    readonly_fields = [
        "variant",
        "change_qty",
        "reason",
        "reference",
        "performed_by",
        "created_at",
    ]
    ordering = ["-created_at"]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False  # Immutable audit log — created only via signals/services

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AttributeSchema)
class AttributeSchemaAdmin(ModelAdmin):
    list_display = [
        "key",
        "label",
        "shop_category",
        "data_type",
        "is_variant",
        "is_filterable",
        "sort_order",
    ]
    list_filter = ["shop_category", "data_type", "is_variant"]


@admin.register(PriceHistory)
class PriceHistoryAdmin(ModelAdmin):
    list_display = ["product", "price", "recorded_at"]
    readonly_fields = ["product", "price", "recorded_at"]
    ordering = ["-recorded_at"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# ─────────────────────────────────────────────────────────────────────────────
# apps/accounts/admin.py
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# apps/shops/admin.py
# ─────────────────────────────────────────────────────────────────────────────
