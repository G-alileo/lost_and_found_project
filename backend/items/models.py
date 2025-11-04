from __future__ import annotations

from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=64)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.category.name} → {self.name}"


