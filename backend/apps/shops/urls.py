from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.ShopCategoryListView.as_view(), name="shop-categories"),
    path("nearby/", views.NearbyShopsView.as_view(), name="shops-nearby"),
    path("mine/", views.MyShopsView.as_view(), name="my-shops"),
    path("", views.ShopListCreateView.as_view(), name="shop-list-create"),
    path("<slug:slug>/", views.ShopDetailView.as_view(), name="shop-detail"),
]
