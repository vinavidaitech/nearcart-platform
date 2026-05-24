"""
apps/core/dashboard.py

Dashboard callback injecting KPIs and chart data into the Unfold admin
dashboard. Place this file at apps/core/dashboard.py and make sure
apps/core/__init__.py exists.
"""

import json
from datetime import timedelta
from decimal import Decimal

from django.db.models import Avg, Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.db.models.functions import TruncDay, TruncMonth
from django.utils import timezone


# ── Sidebar badge callbacks ────────────────────────────────────────────────────


def pending_sales_badge(request):
    """Show count of draft/confirmed sales orders in the sidebar badge."""
    try:
        from apps.billing.models import SalesOrder

        count = SalesOrder.objects.filter(status__in=["draft", "confirmed"]).count()
        return str(count) if count else ""
    except Exception:
        return ""


def unpaid_invoices_badge(request):
    """Show count of issued/partial/overdue invoices in the sidebar badge."""
    try:
        from apps.billing.models import Invoice

        count = Invoice.objects.filter(
            status__in=["issued", "partial", "overdue"]
        ).count()
        return str(count) if count else ""
    except Exception:
        return ""


# ── Environment label ──────────────────────────────────────────────────────────


def environment_callback(request):
    """
    Returns (label, colour) tuple shown as a badge in the admin header.
    Colour options: "info" | "danger" | "warning" | "success"
    """
    from django.conf import settings

    if getattr(settings, "DEBUG", False):
        return "Development", "warning"
    return "Production", "success"


# ── Helpers ────────────────────────────────────────────────────────────────────


def _revenue_chart_data(days: int = 30) -> dict:
    """Daily revenue for the last `days` days as Chart.js-ready JSON."""
    from apps.billing.models import SalesOrder

    cutoff = timezone.now() - timedelta(days=days)
    rows = (
        SalesOrder.objects.filter(
            status="completed",
            completed_at__gte=cutoff,
        )
        .annotate(day=TruncDay("completed_at"))
        .values("day")
        .annotate(revenue=Sum("grand_total"), orders=Count("id"))
        .order_by("day")
    )

    labels, revenues, order_counts = [], [], []
    for row in rows:
        labels.append(row["day"].strftime("%d %b"))
        revenues.append(float(row["revenue"] or 0))
        order_counts.append(row["orders"])

    return {
        "labels": json.dumps(labels),
        "revenues": json.dumps(revenues),
        "order_counts": json.dumps(order_counts),
    }


def _monthly_revenue_chart_data(months: int = 6) -> dict:
    """Monthly revenue for the last `months` months."""
    from apps.billing.models import SalesOrder

    cutoff = timezone.now() - timedelta(days=months * 30)
    rows = (
        SalesOrder.objects.filter(status="completed", completed_at__gte=cutoff)
        .annotate(month=TruncMonth("completed_at"))
        .values("month")
        .annotate(revenue=Sum("grand_total"))
        .order_by("month")
    )
    labels = [r["month"].strftime("%b %Y") for r in rows]
    values = [float(r["revenue"] or 0) for r in rows]
    return {"labels": json.dumps(labels), "values": json.dumps(values)}


def _top_products(limit: int = 8) -> list:
    """Top selling products by revenue in the last 30 days."""
    from apps.billing.models import SalesOrderItem

    cutoff = timezone.now() - timedelta(days=30)
    return list(
        SalesOrderItem.objects.filter(
            sales_order__status="completed",
            sales_order__completed_at__gte=cutoff,
        )
        .values("variant__product__name")
        .annotate(
            units=Sum("quantity"),
            revenue=Sum("line_total"),
        )
        .order_by("-revenue")[:limit]
    )


def _order_status_distribution() -> dict:
    """Doughnut chart data for sales order statuses."""
    from apps.billing.models import SalesOrder

    rows = (
        SalesOrder.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    labels = [r["status"].title() for r in rows]
    values = [r["count"] for r in rows]
    return {"labels": json.dumps(labels), "values": json.dumps(values)}


def _low_stock_products(threshold_override: int | None = None) -> list:
    """Products where total_stock ≤ low_stock_threshold."""
    from apps.inventory.models import Product

    qs = (
        Product.objects.filter(
            is_active=True,
            total_stock__lte=F("low_stock_threshold"),
        )
        .select_related("shop", "category")
        .order_by("total_stock")[:15]
    )
    return list(qs)


def _pending_purchase_orders() -> list:
    """Purchase orders that are SENT or PARTIAL (awaiting delivery)."""
    from apps.billing.models import PurchaseOrder

    return list(
        PurchaseOrder.objects.filter(status__in=["sent", "partial"])
        .select_related("supplier", "shop")
        .order_by("expected_delivery_date")[:10]
    )


def _recent_sales(limit: int = 8) -> list:
    """Most recent completed sales orders."""
    from apps.billing.models import SalesOrder

    return list(
        SalesOrder.objects.filter(status="completed")
        .select_related("customer", "shop", "served_by")
        .order_by("-completed_at")[:limit]
    )


def _stock_movement_chart(days: int = 14) -> dict:
    """Daily stock-in vs stock-out for the last `days` days."""
    from apps.inventory.models import StockMovement

    cutoff = timezone.now() - timedelta(days=days)
    rows = (
        StockMovement.objects.filter(created_at__gte=cutoff)
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(
            stock_in=Sum(
                "change_qty",
                filter=Q(change_qty__gt=0),
            ),
            stock_out=Sum(
                "change_qty",
                filter=Q(change_qty__lt=0),
            ),
        )
        .order_by("day")
    )
    labels = [r["day"].strftime("%d %b") for r in rows]
    stock_in = [float(r["stock_in"] or 0) for r in rows]
    stock_out = [abs(float(r["stock_out"] or 0)) for r in rows]
    return {
        "labels": json.dumps(labels),
        "stock_in": json.dumps(stock_in),
        "stock_out": json.dumps(stock_out),
    }


# ── Main callback ──────────────────────────────────────────────────────────────


def dashboard_callback(request, context: dict) -> dict:
    """
    Called by Unfold before rendering the admin dashboard.
    Injects KPIs, chart data, and table data into the template context.
    """
    now = timezone.now()
    today = now.date()
    month_start = today.replace(day=1)

    try:
        from apps.billing.models import (
            Invoice,
            Payment,
            PurchaseOrder,
            SalesOrder,
        )
        from apps.inventory.models import Product, StockMovement

        # ── KPI cards ─────────────────────────────────────────────────────────

        today_revenue = SalesOrder.objects.filter(
            status="completed", completed_at__date=today
        ).aggregate(s=Sum("grand_total"))["s"] or Decimal("0")

        month_revenue = SalesOrder.objects.filter(
            status="completed",
            completed_at__date__gte=month_start,
        ).aggregate(s=Sum("grand_total"))["s"] or Decimal("0")

        today_orders = SalesOrder.objects.filter(created_at__date=today).count()
        pending_orders = SalesOrder.objects.filter(
            status__in=["draft", "confirmed"]
        ).count()
        unpaid_invoices = Invoice.objects.filter(
            status__in=["issued", "partial", "overdue"]
        ).count()
        unpaid_value = Invoice.objects.filter(
            status__in=["issued", "partial", "overdue"]
        ).aggregate(s=Sum("balance_due"))["s"] or Decimal("0")
        low_stock_count = Product.objects.filter(
            is_active=True,
            total_stock__lte=F("low_stock_threshold"),
        ).count()
        total_products = Product.objects.filter(is_active=True).count()
        pending_pos = PurchaseOrder.objects.filter(
            status__in=["sent", "partial"]
        ).count()

        context["kpis"] = [
            {
                "title": "Today's Revenue",
                "value": f"₹{today_revenue:,.2f}",
                "icon": "payments",
                "color": "success",
            },
            {
                "title": "Month Revenue",
                "value": f"₹{month_revenue:,.2f}",
                "icon": "trending_up",
                "color": "info",
            },
            {
                "title": "Today's Orders",
                "value": today_orders,
                "icon": "receipt_long",
                "color": "info",
            },
            {
                "title": "Pending Orders",
                "value": pending_orders,
                "icon": "pending_actions",
                "color": "warning" if pending_orders > 0 else "success",
            },
            {
                "title": "Unpaid Invoices",
                "value": unpaid_invoices,
                "icon": "description",
                "color": "danger" if unpaid_invoices > 5 else "warning",
            },
            {
                "title": "Unpaid Value",
                "value": f"₹{unpaid_value:,.2f}",
                "icon": "money_off",
                "color": "danger" if unpaid_value > 10000 else "warning",
            },
            {
                "title": "Low Stock Items",
                "value": low_stock_count,
                "icon": "inventory",
                "color": "danger" if low_stock_count > 0 else "success",
            },
            {
                "title": "Active Products",
                "value": total_products,
                "icon": "inventory_2",
                "color": "info",
            },
            {
                "title": "POs Awaiting",
                "value": pending_pos,
                "icon": "local_shipping",
                "color": "warning" if pending_pos > 0 else "success",
            },
        ]

        # ── Charts ────────────────────────────────────────────────────────────
        context["revenue_chart"] = _revenue_chart_data(days=30)
        context["monthly_chart"] = _monthly_revenue_chart_data(months=6)
        context["order_status_chart"] = _order_status_distribution()
        context["stock_movement_chart"] = _stock_movement_chart(days=14)

        # ── Tables ────────────────────────────────────────────────────────────
        context["top_products"] = _top_products(limit=8)
        context["low_stock_products"] = _low_stock_products()
        context["pending_purchase_orders"] = _pending_purchase_orders()
        context["recent_sales"] = _recent_sales(limit=8)

    except Exception as e:
        # Never crash the admin — just pass empty context
        context["dashboard_error"] = str(e)

    return context
