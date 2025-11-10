from __future__ import annotations
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chat.models import Conversation, Message
from chat.serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations"""
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """Return conversations where the user is a participant"""
        user = self.request.user
        return Conversation.objects.filter(
            Q(lost_user=user) | Q(found_user=user)
        ).select_related(
            'lost_user', 'found_user', 'lost_report', 'found_report'
        ).prefetch_related('messages')

    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        """Create a new conversation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if conversation already exists
        lost_report_id = serializer.validated_data['lost_report'].id
        found_report_id = serializer.validated_data['found_report'].id
        
        existing = Conversation.objects.filter(
            lost_report_id=lost_report_id,
            found_report_id=found_report_id
        ).first()
        
        if existing:
            # Return existing conversation
            response_serializer = ConversationSerializer(existing, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        # Create new conversation
        self.perform_create(serializer)
        response_serializer = ConversationSerializer(
            serializer.instance, 
            context={'request': request}
        )
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a conversation"""
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        
        # Mark messages as read for the current user
        Message.objects.filter(
            conversation=conversation
        ).exclude(
            sender=request.user
        ).update(is_read=True)
        
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in a conversation"""
        conversation = self.get_object()
        
        # Verify user is part of the conversation
        if request.user not in [conversation.lost_user, conversation.found_user]:
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create message
        serializer = MessageSerializer(
            data={
                'conversation': conversation.id,
                'content': request.data.get('content')
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        
        # Update conversation timestamp
        conversation.save() 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get total count of unread messages for the user"""
        user = request.user
        unread = Message.objects.filter(
            conversation__in=self.get_queryset()
        ).exclude(
            sender=user
        ).filter(
            is_read=False
        ).count()
        
        return Response({'unread_count': unread})


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing messages (read-only, managed through conversations)"""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        """Return messages from conversations where the user is a participant"""
        user = self.request.user
        return Message.objects.filter(
            Q(conversation__lost_user=user) | Q(conversation__found_user=user)
        ).select_related('sender', 'conversation')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        
        # Only allow marking as read if user is the recipient
        if message.sender == request.user:
            return Response(
                {"error": "Cannot mark your own message as read."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message.is_read = True
        message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
