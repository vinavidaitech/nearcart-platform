from pathlib import Path
from datetime import timedelta
import environ
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


GDAL_LIBRARY_PATH = "/usr/lib/x86_64-linux-gnu/libgdal.so"
GEOS_LIBRARY_PATH = "/usr/lib/x86_64-linux-gnu/libgeos_c.so"


BASE_DIR = Path(__file__).resolve().parent.parent.parent
#           base.py → settings/ → config/ → vinavidai-backend/ ✓

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "unfold",  # must be first
    "unfold.contrib.filters",  # optional but useful
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.postgres",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "storages",
    "apps.accounts",
    "apps.billing",
    "apps.shops",
    "apps.inventory",
    "apps.search",
    "apps.analytics",
    "apps.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ← add this
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
AUTH_USER_MODEL = "accounts.CustomUser"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



DATABASES = {"default": env.db("DATABASE_URL")}

# ✅ FORCE PostGIS engine
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


CELERY_BROKER_URL = env("REDIS_URL")
CELERY_RESULT_BACKEND = env("REDIS_URL")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Vite dev server origin
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:5173"])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=["http://localhost:5173"])

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_SECURE = not DEBUG   # True in production (HTTPS only)
REFRESH_COOKIE_SAMESITE = "Lax"


# ─────────────────────────────────────────────────────────────────────────────
# ADD TO YOUR settings.py
# ─────────────────────────────────────────────────────────────────────────────
#
# 1. Add "unfold" apps BEFORE "django.contrib.admin" in INSTALLED_APPS:
#
# INSTALLED_APPS = [
#     "unfold",
#     "unfold.contrib.filters",
#     "unfold.contrib.forms",
#     "unfold.contrib.inlines",
#     "unfold.contrib.import_export",   # only if you install django-import-export
#     "django.contrib.admin",
#     ... rest of your apps
# ]
#
# 2. Paste the entire UNFOLD dict below into your settings.py
# ─────────────────────────────────────────────────────────────────────────────

UNFOLD = {
    "SITE_TITLE": "Vinavidai",
    "SITE_HEADER": "Vinavidai Admin",
    "SITE_SUBHEADER": "Shop & Inventory Management",
    "SITE_URL": "/",
    "SITE_ICON": None,  # path to your logo, e.g. "images/logo.svg"
    "SITE_SYMBOL": "storefront",  # Material icon shown in sidebar
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "apps.core.dashboard.environment_callback",
    "DASHBOARD_CALLBACK": "apps.core.dashboard.dashboard_callback",
    # ── Sidebar navigation ────────────────────────────────────────────────────
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Analytics"),
                "separator": False,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Billing"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Sales Orders"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:billing_salesorder_changelist"),
                        "badge": "apps.core.dashboard.pending_sales_badge",
                    },
                    {
                        "title": _("Invoices"),
                        "icon": "description",
                        "link": reverse_lazy("admin:billing_invoice_changelist"),
                        "badge": "apps.core.dashboard.unpaid_invoices_badge",
                    },
                    {
                        "title": _("Purchase Orders"),
                        "icon": "shopping_cart",
                        "link": reverse_lazy("admin:billing_purchaseorder_changelist"),
                    },
                    {
                        "title": _("Payments"),
                        "icon": "payments",
                        "link": reverse_lazy("admin:billing_payment_changelist"),
                    },
                    {
                        "title": _("Returns"),
                        "icon": "assignment_return",
                        "link": reverse_lazy("admin:billing_return_changelist"),
                    },
                    {
                        "title": _("Customers"),
                        "icon": "people",
                        "link": reverse_lazy("admin:billing_customer_changelist"),
                    },
                    {
                        "title": _("Suppliers"),
                        "icon": "local_shipping",
                        "link": reverse_lazy("admin:billing_supplier_changelist"),
                    },
                    {
                        "title": _("Discounts"),
                        "icon": "loyalty",
                        "link": reverse_lazy("admin:billing_discount_changelist"),
                    },
                    {
                        "title": _("Tax Rates"),
                        "icon": "percent",
                        "link": reverse_lazy("admin:billing_taxrate_changelist"),
                    },
                    {
                        "title": _("Bulk Imports"),
                        "icon": "upload_file",
                        "link": reverse_lazy("admin:billing_bulkimport_changelist"),
                    },
                ],
            },
            {
                "title": _("Inventory"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Products"),
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:inventory_product_changelist"),
                    },
                    {
                        "title": _("Product Variants"),
                        "icon": "style",
                        "link": reverse_lazy(
                            "admin:inventory_productvariant_changelist"
                        ),
                    },
                    {
                        "title": _("Stock Movements"),
                        "icon": "swap_vert",
                        "link": reverse_lazy(
                            "admin:inventory_stockmovement_changelist"
                        ),
                    },
                    {
                        "title": _("Brands"),
                        "icon": "verified",
                        "link": reverse_lazy("admin:inventory_brand_changelist"),
                    },
                    {
                        "title": _("Categories"),
                        "icon": "category",
                        "link": reverse_lazy(
                            "admin:inventory_productcategory_changelist"
                        ),
                    },
                    {
                        "title": _("Locations"),
                        "icon": "place",
                        "link": reverse_lazy("admin:inventory_locationnode_changelist"),
                    },
                    {
                        "title": _("Price History"),
                        "icon": "trending_up",
                        "link": reverse_lazy("admin:inventory_pricehistory_changelist"),
                    },
                ],
            },
            {
                "title": _("Shops"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Shops"),
                        "icon": "storefront",
                        "link": reverse_lazy("admin:shops_shop_changelist"),
                    },
                    {
                        "title": _("Shop Categories"),
                        "icon": "workspaces",
                        "link": reverse_lazy("admin:shops_shopcategory_changelist"),
                    },
                ],
            },
            {
                "title": _("Users"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:accounts_customuser_changelist"),
                    },
                    {
                        "title": _("Staff Memberships"),
                        "icon": "badge",
                        "link": reverse_lazy(
                            "admin:accounts_staffmembership_changelist"
                        ),
                    },
                ],
            },
        ],
    },
    # ── Tabs on the change form ───────────────────────────────────────────────
    "TABS": [
        {
            "models": ["billing.salesorder"],
            "items": [
                {
                    "title": _("Order Details"),
                    "link": reverse_lazy("admin:billing_salesorder_changelist"),
                },
                {
                    "title": _("Invoices"),
                    "link": reverse_lazy("admin:billing_invoice_changelist"),
                },
                {
                    "title": _("Returns"),
                    "link": reverse_lazy("admin:billing_return_changelist"),
                },
            ],
        },
    ],
}
