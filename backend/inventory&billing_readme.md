# ─────────────────────────────────────────────────────────────────────────────

# apps/inventory/urls.py

# ─────────────────────────────────────────────────────────────────────────────

# from django.urls import path, include

# from rest_framework.routers import DefaultRouter

# from . import views

#

# router = DefaultRouter()

# router.register('products', views.ProductViewSet, basename='product')

# router.register('variants', views.ProductVariantViewSet, basename='variant')

# router.register('locations', views.LocationNodeViewSet, basename='location')

# router.register('categories', views.ProductCategoryViewSet, basename='category')

# router.register('brands', views.BrandViewSet, basename='brand')

# router.register('movements', views.StockMovementViewSet, basename='movement')

#

# urlpatterns = [path('', include(router.urls))]

# ─────────────────────────────────────────────────────────────────────────────

# apps/billing/urls.py

# ─────────────────────────────────────────────────────────────────────────────

# from django.urls import path, include

# from rest_framework.routers import DefaultRouter

# from . import views

#

# router = DefaultRouter()

# router.register('suppliers', views.SupplierViewSet, basename='supplier')

# router.register('customers', views.CustomerViewSet, basename='customer')

# router.register('tax-rates', views.TaxRateViewSet, basename='taxrate')

# router.register('discounts', views.DiscountViewSet, basename='discount')

# router.register('purchase-orders', views.PurchaseOrderViewSet, basename='purchaseorder')

# router.register('sales-orders', views.SalesOrderViewSet, basename='salesorder')

# router.register('invoices', views.InvoiceViewSet, basename='invoice')

# router.register('payments', views.PaymentViewSet, basename='payment')

# router.register('returns', views.ReturnViewSet, basename='return')

#

# urlpatterns = [path('', include(router.urls))]

# ─────────────────────────────────────────────────────────────────────────────

# config/urls.py (add these two lines to your main urlconf)

# ─────────────────────────────────────────────────────────────────────────────

# path('api/inventory/', include('apps.inventory.urls'))

# path('api/billing/', include('apps.billing.urls'))

# ═════════════════════════════════════════════════════════════════════════════

# COMPLETE ENDPOINT REFERENCE

# ═════════════════════════════════════════════════════════════════════════════

#

# All endpoints require

# Authorization: Bearer <access_token>

# X-Shop-ID: <shop_uuid> ← required for shop-scoped resources

#

# ── INVENTORY ─────────────────────────────────────────────────────────────────

#

# Products

# GET /api/inventory/products/ list (search, category, stock_status)

# POST /api/inventory/products/ create

# GET /api/inventory/products/{id}/ detail

# PUT /api/inventory/products/{id}/ update

# PATCH /api/inventory/products/{id}/ partial update

# DELETE /api/inventory/products/{id}/ soft-delete

# POST /api/inventory/products/{id}/adjust-stock/ manual qty adjustment

# GET /api/inventory/products/{id}/movements/ stock history

# GET /api/inventory/products/{id}/images/ list images

# POST /api/inventory/products/{id}/images/ add image

# GET /api/inventory/products/low-stock/ products at/below threshold

# GET /api/inventory/products/out-of-stock/ products with 0 stock

#

# Variants

# GET /api/inventory/variants/?product={id} list variants

# POST /api/inventory/variants/ create variant

# PATCH /api/inventory/variants/{id}/ update

# DELETE /api/inventory/variants/{id}/ soft-delete

#

# Locations

# GET /api/inventory/locations/ list (parent=root for top-level)

# POST /api/inventory/locations/ create

# PUT /api/inventory/locations/{id}/ update

# DELETE /api/inventory/locations/{id}/ soft-delete

#

# Reference (read-only)

# GET /api/inventory/categories/ product categories

# GET /api/inventory/brands/ brands

# GET /api/inventory/movements/ all stock movements

#

# ── BILLING ───────────────────────────────────────────────────────────────────

#

# Customers

# GET /api/billing/customers/ list (search by name/phone)

# POST /api/billing/customers/ create

# GET /api/billing/customers/{id}/ detail

# PUT /api/billing/customers/{id}/ update

# GET /api/billing/customers/{id}/orders/ order history

#

# Suppliers

# GET /api/billing/suppliers/ list

# POST /api/billing/suppliers/ create

# PUT /api/billing/suppliers/{id}/ update

# DELETE /api/billing/suppliers/{id}/ soft-delete

#

# Sales Orders (POS)

# GET /api/billing/sales-orders/ list (status, customer, date_from, date_to)

# POST /api/billing/sales-orders/ create (with items array)

# GET /api/billing/sales-orders/{id}/ detail

# PATCH /api/billing/sales-orders/{id}/ update

# POST /api/billing/sales-orders/{id}/complete/ pay → deduct stock → gen invoice

# POST /api/billing/sales-orders/{id}/cancel/ cancel

# GET /api/billing/sales-orders/summary/ today's revenue summary

#

# Purchase Orders

# GET /api/billing/purchase-orders/ list (status, supplier)

# POST /api/billing/purchase-orders/ create (with items array)

# GET /api/billing/purchase-orders/{id}/ detail

# PATCH /api/billing/purchase-orders/{id}/ update

# POST /api/billing/purchase-orders/{id}/receive/ mark received → restock

# GET /api/billing/purchase-orders/{id}/items/ list items

# POST /api/billing/purchase-orders/{id}/items/ add item

#

# Invoices

# GET /api/billing/invoices/ list (status filter)

# GET /api/billing/invoices/{id}/ detail

#

# Payments

# GET /api/billing/payments/?invoice={id} list

# POST /api/billing/payments/ record payment

#

# Returns

# GET /api/billing/returns/ list

# POST /api/billing/returns/ create return request

# PATCH /api/billing/returns/{id}/ update

# POST /api/billing/returns/{id}/approve/ approve + restock

#

# Tax Rates

# GET /api/billing/tax-rates/ list

# POST /api/billing/tax-rates/ create

#

# Discounts

# GET /api/billing/discounts/ list

# POST /api/billing/discounts/ create

# POST /api/billing/discounts/validate/ validate code {code, order_total}
