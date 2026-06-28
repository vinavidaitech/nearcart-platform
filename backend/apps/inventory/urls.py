from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products',   views.ProductViewSet,      basename='product')
router.register('variants',   views.ProductVariantViewSet, basename='variant')
router.register('locations',  views.LocationNodeViewSet,  basename='location')
router.register('categories', views.ProductCategoryViewSet, basename='category')
router.register('brands',     views.BrandViewSet,         basename='brand')
router.register('movements',  views.StockMovementViewSet, basename='movement')

urlpatterns = [path('', include(router.urls))]
