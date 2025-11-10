from __future__ import annotations
from rest_framework import serializers
from chat.models import Conversation, Message
from users.models import User
from reports.models import Report


class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user information for chat"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture']


class ReportBasicSerializer(serializers.ModelSerializer):
    """Basic report information for chat"""
    class Meta:
        model = Report
        fields = ['id', 'title', 'report_type', 'status']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages"""
    sender = UserBasicSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_id', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Set sender from request user if not provided
        if 'sender_id' not in validated_data:
            validated_data['sender'] = self.context['request'].user
        else:
            validated_data['sender_id'] = validated_data.pop('sender_id')
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversations"""
    lost_user = UserBasicSerializer(read_only=True)
    found_user = UserBasicSerializer(read_only=True)
    lost_report = ReportBasicSerializer(read_only=True)
    found_report = ReportBasicSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'lost_report', 'found_report', 'lost_user', 'found_user',
            'created_at', 'updated_at', 'is_active', 'last_message', 'unread_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        """Get the last message in the conversation"""
        last_message = obj.messages.last()
        if last_message:
            return {
                'id': last_message.id,
                'sender': last_message.sender.username,
                'content': last_message.content,
                'created_at': last_message.created_at
            }
        return None

    def get_unread_count(self, obj):
        """Get count of unread messages for the current user"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating conversations (supports both matched and single-item conversations)"""
    lost_report_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    found_report_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    report_id = serializers.IntegerField(write_only=True, required=False, help_text="Single report ID for simple conversations")

    class Meta:
        model = Conversation
        fields = ['id', 'lost_report_id', 'found_report_id', 'report_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        """Validate that at least one report is provided"""
        request = self.context.get('request')
        current_user = request.user if request and request.user.is_authenticated else None
        
        # Case 1: Simple conversation about a single report
        if 'report_id' in attrs and attrs['report_id']:
            try:
                report = Report.objects.get(id=attrs['report_id'])
            except Report.DoesNotExist:
                raise serializers.ValidationError("Report does not exist.")
            
            # Prevent messaging yourself
            if report.reported_by == current_user:
                raise serializers.ValidationError("You cannot start a conversation with yourself.")
            
            # Set up conversation participants
            if report.report_type == 'lost':
                attrs['lost_report'] = report
                attrs['found_report'] = None
                attrs['lost_user'] = report.reported_by
                attrs['found_user'] = current_user
            else:  # found
                attrs['found_report'] = report
                attrs['lost_report'] = None
                attrs['found_user'] = report.reported_by
                attrs['lost_user'] = current_user
            
            attrs.pop('report_id')
            return attrs
        
        # Case 2: Matched conversation (old behavior)
        if 'lost_report_id' not in attrs or 'found_report_id' not in attrs:
            raise serializers.ValidationError("Either report_id or both lost_report_id and found_report_id must be provided.")
        
        try:
            lost_report = Report.objects.get(id=attrs['lost_report_id'])
            found_report = Report.objects.get(id=attrs['found_report_id'])
        except Report.DoesNotExist:
            raise serializers.ValidationError("One or both reports do not exist.")

        if lost_report.report_type != 'lost':
            raise serializers.ValidationError("lost_report_id must reference a lost report.")
        if found_report.report_type != 'found':
            raise serializers.ValidationError("found_report_id must reference a found report.")

        attrs['lost_report'] = lost_report
        attrs['found_report'] = found_report
        attrs['lost_user'] = lost_report.reported_by
        attrs['found_user'] = found_report.reported_by

        # Check if user is authorized to create this conversation
        if current_user:
            if current_user not in [attrs['lost_user'], attrs['found_user']]:
                raise serializers.ValidationError(
                    "You can only create conversations for your own reports."
                )

        return attrs

    def create(self, validated_data):
        # Remove IDs before creating
        validated_data.pop('lost_report_id', None)
        validated_data.pop('found_report_id', None)
        
        # Check if conversation already exists
        lost_report = validated_data.get('lost_report')
        found_report = validated_data.get('found_report')
        lost_user = validated_data.get('lost_user')
        found_user = validated_data.get('found_user')
        
        # Try to find existing conversation between these users about these reports
        existing = Conversation.objects.filter(
            lost_report=lost_report,
            found_report=found_report,
            lost_user=lost_user,
            found_user=found_user
        ).first()
        
        if existing:
            return existing
        
        return super().create(validated_data)
