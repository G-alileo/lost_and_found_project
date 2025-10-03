from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "report_type", "status", "category", "reported_by", "created_at")
    list_filter = ("report_type", "status", "category", "created_at")
    search_fields = ("title", "description", "location")


