from __future__ import annotations

from rest_framework import serializers

from .models import ImageMatchLog


class ImageMatchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageMatchLog
        fields = ["id", "image", "suggestions", "created_at"]
        read_only_fields = ["id", "suggestions", "created_at"]


