from __future__ import annotations

from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "description",
            "category",
            "report_type",
            "status",
            "reported_by",
            "image",
            "location",
            "date_lost_found",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reported_by", "status", "created_at", "updated_at"]


class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "title", "category", "report_type", "image", "location", "created_at"]


