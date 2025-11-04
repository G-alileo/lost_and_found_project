from __future__ import annotations

import re

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile_picture', read_only=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "profile_picture",
            "avatar",
            "bio",
        ]
        read_only_fields = ["id", "role"]


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile_picture', required=False)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "profile_picture", "avatar", "bio"]


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    
    def validate_new_password(self, value):
        # Add password validation if needed
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value):
            raise serializers.ValidationError("Password must contain at least 8 characters, including uppercase, lowercase, digits, and special characters.")
        return value


