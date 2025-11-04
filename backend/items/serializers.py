from __future__ import annotations

from rest_framework import serializers

from .models import Category, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "category", "name", "created_by", "created_at"]
        read_only_fields = ["id", "created_by", "created_at"]


