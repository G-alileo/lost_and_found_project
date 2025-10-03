from __future__ import annotations

from django.conf import settings
from django.db import models

from items.models import Category


class Report(models.Model):
    class ReportType(models.TextChoices):
        LOST = "lost", "Lost"
        FOUND = "found", "Found"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        MATCHED = "matched", "Matched"
        CLAIMED = "claimed", "Claimed"
        UNCLAIMED = "unclaimed", "Unclaimed"

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    report_type = models.CharField(max_length=8, choices=ReportType.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="reports/", null=True, blank=True)
    location = models.TextField()
    date_lost_found = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.report_type}: {self.title}"


