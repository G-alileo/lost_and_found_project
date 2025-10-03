from __future__ import annotations

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and (getattr(user, "role", None) == "admin" or user.is_staff))


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, "role", None) == "admin" or user.is_staff:
            return True
        owner = getattr(obj, "reported_by", None) or getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == user


