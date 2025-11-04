from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "student", "Student"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, choices=Roles.choices)
    profile_picture = models.ImageField(upload_to="users/", null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self) -> str:  
        return self.username


