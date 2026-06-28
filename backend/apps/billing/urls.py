from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('suppliers',       views.SupplierViewSet,       basename='supplier')
router.register('customers',       views.CustomerViewSet,        basename='customer')
router.register('tax-rates',       views.TaxRateViewSet,         basename='taxrate')
router.register('discounts',       views.DiscountViewSet,        basename='discount')
router.register('purchase-orders', views.PurchaseOrderViewSet,   basename='purchaseorder')
router.register('sales-orders',    views.SalesOrderViewSet,      basename='salesorder')
router.register('invoices',        views.InvoiceViewSet,         basename='invoice')
router.register('payments',        views.PaymentViewSet,         basename='payment')
router.register('returns',         views.ReturnViewSet,          basename='return')

urlpatterns = [path('', include(router.urls))]
