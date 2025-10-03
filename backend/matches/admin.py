from django.contrib import admin

from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "lost_report", "found_report", "confidence_score", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("lost_report__title", "found_report__title")


