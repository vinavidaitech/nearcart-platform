from apps.shops.models import Shop, ShopCategory, ShopImage
from django.contrib import admin
from unfold.decorators import action, display


# Register your models here.
# admin.site.register(ShopCategory)
# admin.site.register(Shop)
# admin.site.register(ShopImage)

# Already configured
from unfold.admin import ModelAdmin, StackedInline, TabularInline


class ShopImageInline(TabularInline):
    model = ShopImage
    extra = 0
    fields = ["url", "alt_text", "is_cover", "sort_order"]


@admin.register(Shop)
class ShopAdmin(ModelAdmin):
    list_display = [
        "name",
        "owner",
        "primary_category",
        "city",
        "status_badge",
        "is_verified",
        "rating",
        "created_at",
    ]
    list_filter = ["status", "is_verified", "primary_category", "city"]
    search_fields = ["name", "slug", "city", "owner__email", "owner__full_name"]
    readonly_fields = ["slug", "created_at", "updated_at", "latitude", "longitude"]
    inlines = [ShopImageInline]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Identity",
            {"fields": ("name", "slug", "owner", "primary_category", "description")},
        ),
        (
            "Location",
            {
                "fields": (
                    "address_line",
                    "city",
                    "location",
                    "latitude",
                    "longitude",
                    "google_place_id",
                    "floor_plan_url",
                )
            },
        ),
        ("Contact", {"fields": ("phone", "email", "website")}),
        ("Status", {"fields": ("status", "is_verified")}),
        ("Stats", {"fields": ("rating", "total_reviews", "opening_hours")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @display(description="Status", label=True)
    def status_badge(self, obj):
        colours = {
            "pending": "yellow",
            "active": "green",
            "suspended": "red",
            "closed": "gray",
        }
        return obj.status, colours.get(obj.status, "gray")

    @admin.display(description="Latitude")
    def latitude(self, obj):
        return obj.latitude

    @admin.display(description="Longitude")
    def longitude(self, obj):
        return obj.longitude


@admin.register(ShopCategory)
class ShopCategoryAdmin(ModelAdmin):
    list_display = ["name", "slug", "sort_order", "is_active"]
    list_editable = ["sort_order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]
