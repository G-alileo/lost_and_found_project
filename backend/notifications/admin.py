from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_read", "created_at", "related_match")
    list_filter = ("is_read", "created_at")
    search_fields = ("message", "user__username")


