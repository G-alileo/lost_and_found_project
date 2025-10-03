from __future__ import annotations

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reports"

    def ready(self) -> None:  # pragma: no cover
        from . import signals  # noqa: F401


