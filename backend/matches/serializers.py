from __future__ import annotations

from rest_framework import serializers

from .models import Match
from reports.serializers import ReportSerializer


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ["id", "lost_report", "found_report", "confidence_score", "status", "created_at", "resolved_at"]
        read_only_fields = ["id", "created_at", "resolved_at"]


class MatchDetailSerializer(serializers.ModelSerializer):
    lost_report = ReportSerializer(read_only=True)
    found_report = ReportSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ["id", "lost_report", "found_report", "confidence_score", "status", "created_at", "resolved_at"]


