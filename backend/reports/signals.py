from __future__ import annotations
from django.db.models.signals import post_save
from django.dispatch import receiver
from matches.services import run_matching_for_report
from .models import Report


@receiver(post_save, sender=Report)
def trigger_matching(sender, instance: Report, created: bool, **kwargs):
    if created:
        run_matching_for_report(instance)


