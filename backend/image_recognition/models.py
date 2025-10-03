from __future__ import annotations

from django.conf import settings
from django.db import models


class ImageMatchLog(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="image_recognition/")
    suggestions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


