from django.contrib import admin

from .models import ImageMatchLog


@admin.register(ImageMatchLog)
class ImageMatchLogAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_by", "created_at")
    list_filter = ("created_at",)


