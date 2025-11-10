from __future__ import annotations
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from items.models import Category
from reports.models import Report
from chat.models import Conversation, Message

User = get_user_model()


class ChatSystemTestCase(TestCase):
    """Test cases for the chat system"""

    def setUp(self):
        """Set up test data"""
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123',
            role='student'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123',
            role='student'
        )

        # Create category
        self.category = Category.objects.create(name='Electronics')

        # Create lost report
        self.lost_report = Report.objects.create(
            title='Lost iPhone',
            description='Black iPhone 14',
            category=self.category,
            report_type='lost',
            reported_by=self.user1,
            location='Library',
            date_lost_found=date(2025, 11, 1)
        )

        # Create found report
        self.found_report = Report.objects.create(
            title='Found iPhone',
            description='Found a black iPhone',
            category=self.category,
            report_type='found',
            reported_by=self.user2,
            location='Library',
            date_lost_found=date(2025, 11, 2)
        )

        # Set up API client
        self.client = APIClient()

    def test_create_conversation(self):
        """Test creating a conversation between lost and found reports"""
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.post('/api/chat/conversations/', {
            'lost_report_id': self.lost_report.id,
            'found_report_id': self.found_report.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 1)
        
        conversation = Conversation.objects.first()
        self.assertEqual(conversation.lost_user, self.user1)
        self.assertEqual(conversation.found_user, self.user2)

    def test_send_message(self):
        """Test sending a message in a conversation"""
        # Create conversation
        conversation = Conversation.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            lost_user=self.user1,
            found_user=self.user2
        )

        self.client.force_authenticate(user=self.user1)
        
        response = self.client.post(
            f'/api/chat/conversations/{conversation.id}/send_message/',
            {'content': 'Is this my phone?'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        
        message = Message.objects.first()
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.content, 'Is this my phone?')
        self.assertFalse(message.is_read)

    def test_get_messages(self):
        """Test retrieving messages from a conversation"""
        # Create conversation with messages
        conversation = Conversation.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            lost_user=self.user1,
            found_user=self.user2
        )
        
        Message.objects.create(
            conversation=conversation,
            sender=self.user1,
            content='Hello'
        )
        Message.objects.create(
            conversation=conversation,
            sender=self.user2,
            content='Hi there'
        )

        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get(
            f'/api/chat/conversations/{conversation.id}/messages/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthorized_access(self):
        """Test that users cannot access conversations they're not part of"""
        # Create a third user
        user3 = User.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='testpass123',
            role='student'
        )

        conversation = Conversation.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            lost_user=self.user1,
            found_user=self.user2
        )

        self.client.force_authenticate(user=user3)
        
        response = self.client.post(
            f'/api/chat/conversations/{conversation.id}/send_message/',
            {'content': 'Unauthorized message'}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unread_count(self):
        """Test unread message count"""
        conversation = Conversation.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            lost_user=self.user1,
            found_user=self.user2
        )
        
        # User2 sends messages to user1
        Message.objects.create(
            conversation=conversation,
            sender=self.user2,
            content='Message 1',
            is_read=False
        )
        Message.objects.create(
            conversation=conversation,
            sender=self.user2,
            content='Message 2',
            is_read=False
        )

        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get('/api/chat/conversations/unread_count/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 2)
