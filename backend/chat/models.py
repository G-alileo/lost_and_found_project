from __future__ import annotations
from django.conf import settings
from django.db import models
from reports.models import Report


class Conversation(models.Model):
    """
    Represents a conversation between two users about specific lost and found reports.
    A conversation can be about a single item or a match between lost and found items.
    """
    lost_report = models.ForeignKey(
        'reports.Report',
        on_delete=models.CASCADE,
        related_name='lost_conversations',
        null=True,
        blank=True,
        help_text="The lost report this conversation is about (optional)"
    )
    found_report = models.ForeignKey(
        'reports.Report',
        on_delete=models.CASCADE,
        related_name='found_conversations',
        null=True,
        blank=True,
        help_text="The found report this conversation is about (optional)"
    )
    lost_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lost_conversations",
        help_text="User who lost the item"
    )
    found_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="found_conversations",
        help_text="User who found the item"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def clean(self):
        """Validate that at least one report is provided"""
        from django.core.exceptions import ValidationError
        if not self.lost_report and not self.found_report:
            raise ValidationError("At least one report (lost or found) must be provided")
    
    def save(self, *args, **kwargs):
        """Override save to run validation"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        if self.lost_report and self.found_report:
            return f"Conversation: {self.lost_user.username} ↔ {self.found_user.username}"
        elif self.lost_report:
            return f"Conversation about: {self.lost_report.title}"
        else:
            return f"Conversation about: {self.found_report.title}"

    def get_other_user(self, user):
        """Returns the other user in the conversation"""
        return self.found_user if user == self.lost_user else self.lost_user
    
    def get_report(self):
        """Returns the primary report (lost or found)"""
        return self.lost_report or self.found_report


class Message(models.Model):
    """Represents a message in a conversation"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return f"{self.sender.username}: {self.content[:50]}"
