from __future__ import annotations

from django.conf import settings
from django.db import models

from matches.models import Match


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    related_match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"Notif to {self.user_id}: {self.message[:30]}"


