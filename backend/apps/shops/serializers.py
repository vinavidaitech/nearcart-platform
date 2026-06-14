from rest_framework import serializers, generics, permissions
from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from .models import Shop, ShopCategory, ShopImage


class ShopCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopCategory
        fields = "__all__"


class ShopImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopImage
        fields = "__all__"

class ShopSerializer(serializers.ModelSerializer):
    images = ShopImageSerializer(many=True, read_only=True)
    category = ShopCategorySerializer(source="primary_category", read_only=True)
    primary_category = serializers.PrimaryKeyRelatedField(
        queryset=ShopCategory.objects.all(), write_only=True
    )
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)
    lat = serializers.FloatField(write_only=True, required=False)
    lng = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = Shop
        fields = [
            "id", "owner", "category", "primary_category", "name", "slug",
            "description", "address_line", "city", "latitude", "longitude",
            "lat", "lng", "google_place_id", "opening_hours", "phone",
            "email", "website", "status", "is_verified", "rating",
            "total_reviews", "floor_plan_url", "images",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "owner", "slug", "status", "is_verified",
            "rating", "total_reviews", "created_at", "updated_at",
        ]

    def validate(self, attrs):
        lat = attrs.pop("lat", None)
        lng = attrs.pop("lng", None)
        if lat is not None and lng is not None:
            attrs["location"] = Point(lng, lat, srid=4326)
        elif self.instance is None:
            # Creating a new shop — location is mandatory
            raise serializers.ValidationError(
                {"lat": "lat and lng are required to create a shop."}
            )
        return attrs
