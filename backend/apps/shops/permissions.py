# apps/shops/permissions.py
from rest_framework import permissions


class IsShopOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can read; only the shop's owner can modify or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner_id == request.user.id
