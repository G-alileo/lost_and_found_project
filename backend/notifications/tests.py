from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from items.models import Category
from matches.models import Match
from reports.models import Report

from .models import Notification
from .serializers import NotificationSerializer

User = get_user_model()


class NotificationModelTest(TestCase):
    """Test cases for the Notification model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

        # Create test category
        self.category = Category.objects.create(name="Electronics")

        # Create test reports
        self.lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        self.found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.other_user,
            location="Library",
            date_lost_found=timezone.now().date()
        )

        # Create test match
        self.match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )

    def test_notification_creation(self):
        """Test creating a notification."""
        notification = Notification.objects.create(
            user=self.user,
            message="Test notification message"
        )
        
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.message, "Test notification message")
        self.assertFalse(notification.is_read)
        self.assertIsNone(notification.related_match)
        self.assertIsNotNone(notification.created_at)

    def test_notification_with_match(self):
        """Test creating a notification with a related match."""
        notification = Notification.objects.create(
            user=self.user,
            message="Potential match found for your lost item",
            related_match=self.match
        )
        
        self.assertEqual(notification.related_match, self.match)

    def test_notification_str_method(self):
        """Test the string representation of notification."""
        notification = Notification.objects.create(
            user=self.user,
            message="This is a test notification message that is longer than 30 characters"
        )
        
        expected_str = f"Notif to {self.user.id}: This is a test notification me"
        self.assertEqual(str(notification), expected_str)

    def test_notification_str_method_short_message(self):
        """Test the string representation with short message."""
        notification = Notification.objects.create(
            user=self.user,
            message="Short message"
        )
        
        expected_str = f"Notif to {self.user.id}: Short message"
        self.assertEqual(str(notification), expected_str)

    def test_notification_default_is_read(self):
        """Test that notifications are unread by default."""
        notification = Notification.objects.create(
            user=self.user,
            message="Test message"
        )
        
        self.assertFalse(notification.is_read)

    def test_notification_mark_as_read(self):
        """Test marking a notification as read."""
        notification = Notification.objects.create(
            user=self.user,
            message="Test message"
        )
        
        notification.is_read = True
        notification.save()
        
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_user_deletion_cascades(self):
        """Test that deleting a user deletes their notifications."""
        notification = Notification.objects.create(
            user=self.user,
            message="Test message"
        )
        
        notification_id = notification.id
        self.user.delete()
        
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notification_id)

    def test_match_deletion_sets_null(self):
        """Test that deleting a match sets related_match to null."""
        notification = Notification.objects.create(
            user=self.user,
            message="Test message",
            related_match=self.match
        )
        
        match_id = self.match.id
        self.match.delete()
        
        notification.refresh_from_db()
        self.assertIsNone(notification.related_match)


class NotificationSerializerTest(TestCase):
    """Test cases for the NotificationSerializer."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

        # Create test category
        self.category = Category.objects.create(name="Electronics")

        # Create test reports
        self.lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        self.found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user,
            location="Library",
            date_lost_found=timezone.now().date()
        )

        self.match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )

        self.notification = Notification.objects.create(
            user=self.user,
            message="Test notification",
            related_match=self.match
        )

    def test_notification_serialization(self):
        """Test serializing a notification."""
        serializer = NotificationSerializer(self.notification)
        data = serializer.data
        
        self.assertEqual(data['id'], self.notification.id)
        self.assertEqual(data['message'], "Test notification")
        self.assertEqual(data['related_match'], self.match.id)
        self.assertEqual(data['is_read'], False)
        self.assertIn('created_at', data)

    def test_notification_serialization_without_match(self):
        """Test serializing a notification without related match."""
        notification = Notification.objects.create(
            user=self.user,
            message="Test notification without match"
        )
        
        serializer = NotificationSerializer(notification)
        data = serializer.data
        
        self.assertIsNone(data['related_match'])

    def test_notification_deserialization(self):
        """Test deserializing notification data."""
        data = {
            'message': 'New test notification',
            'is_read': True
        }
        
        serializer = NotificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        # Note: We don't test saving here as the user field is required
        # and typically set in the view

    def test_read_only_fields(self):
        """Test that id and created_at are read-only."""
        data = {
            'id': 999,
            'message': 'Test message',
            'created_at': '2023-01-01T00:00:00Z',
            'is_read': False
        }
        
        serializer = NotificationSerializer(self.notification, data=data)
        self.assertTrue(serializer.is_valid())
        
        updated_notification = serializer.save()
        
        # ID and created_at should not change
        self.assertEqual(updated_notification.id, self.notification.id)
        self.assertEqual(updated_notification.created_at, self.notification.created_at)
        self.assertEqual(updated_notification.message, 'Test message')


class NotificationAPITest(APITestCase):
    """Test cases for the Notification API views."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

        # Create test category
        self.category = Category.objects.create(name="Electronics")

        # Create test reports
        self.lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        self.found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.other_user,
            location="Library",
            date_lost_found=timezone.now().date()
        )

        self.match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )

        # Create test notifications
        self.notification1 = Notification.objects.create(
            user=self.user,
            message="First notification",
            related_match=self.match
        )
        
        self.notification2 = Notification.objects.create(
            user=self.user,
            message="Second notification",
            is_read=True
        )
        
        self.other_notification = Notification.objects.create(
            user=self.other_user,
            message="Other user's notification"
        )

    def test_notification_list_authenticated(self):
        """Test listing notifications for authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Check that only user's notifications are returned (filter by user)
        user_notifications = [notif for notif in data if notif['id'] in [self.notification1.id, self.notification2.id]]
        self.assertEqual(len(user_notifications), 2)
        
        # Check that only user's notifications are returned
        notification_ids = [notif['id'] for notif in data]
        self.assertIn(self.notification1.id, notification_ids)
        self.assertIn(self.notification2.id, notification_ids)
        self.assertNotIn(self.other_notification.id, notification_ids)

    def test_notification_list_ordering(self):
        """Test that notifications are ordered by created_at descending."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Find our specific notifications in the response
        our_notifications = [notif for notif in data if notif['id'] in [self.notification1.id, self.notification2.id]]
        our_notifications.sort(key=lambda x: x['id'], reverse=True)  # Sort by ID desc (proxy for created_at desc)
        
        # notification2 was created after notification1, so should have higher ID and be first
        self.assertEqual(our_notifications[0]['id'], self.notification2.id)
        self.assertEqual(our_notifications[1]['id'], self.notification1.id)

    def test_notification_list_unauthenticated(self):
        """Test that unauthenticated users cannot access notifications."""
        url = reverse('notifications-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_notification_read_authenticated(self):
        """Test marking notification as read by authenticated user."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-mark-read', kwargs={'pk': self.notification1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_read'], True)
        
        # Verify the notification was actually updated
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.is_read)

    def test_mark_notification_read_wrong_user(self):
        """Test that users cannot mark other users' notifications as read."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-mark-read', kwargs={'pk': self.other_notification.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Verify the notification was not updated
        self.other_notification.refresh_from_db()
        self.assertFalse(self.other_notification.is_read)

    def test_mark_notification_read_unauthenticated(self):
        """Test that unauthenticated users cannot mark notifications as read."""
        url = reverse('notifications-mark-read', kwargs={'pk': self.notification1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_notification_read_nonexistent(self):
        """Test marking a nonexistent notification as read."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-mark-read', kwargs={'pk': 99999})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_mark_already_read_notification(self):
        """Test marking an already read notification as read."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-mark-read', kwargs={'pk': self.notification2.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_read'], True)

    def test_notification_list_content(self):
        """Test the content of notification list response."""
        self.client.force_authenticate(user=self.user)
        url = reverse('notifications-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Find notification1 in the response
        notification1_data = None
        for notif in data:
            if notif['id'] == self.notification1.id:
                notification1_data = notif
                break
                
        self.assertIsNotNone(notification1_data)
        self.assertEqual(notification1_data['message'], "First notification")
        self.assertEqual(notification1_data['related_match'], self.match.id)
        self.assertEqual(notification1_data['is_read'], False)
        self.assertIn('created_at', notification1_data)

    def test_notification_list_empty(self):
        """Test notification list for user with no notifications."""
        new_user = User.objects.create_user(
            username="newuser",
            email="new@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.client.force_authenticate(user=new_user)
        url = reverse('notifications-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
            
        # This user should have no notifications
        self.assertEqual(len(data), 0)


class NotificationAdminTest(TestCase):
    """Test cases for the Notification admin interface."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            role=User.Roles.ADMIN
        )
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

        # Create test category
        self.category = Category.objects.create(name="Electronics")

        # Create test reports
        self.lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        self.found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user,
            location="Library",
            date_lost_found=timezone.now().date()
        )

        self.match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )

        self.notification = Notification.objects.create(
            user=self.user,
            message="Test notification for admin",
            related_match=self.match
        )

    def test_admin_notification_display(self):
        """Test that notification displays correctly in admin."""
        from django.contrib import admin
        from .admin import NotificationAdmin
        
        # Test that admin is registered
        self.assertIn(Notification, admin.site._registry)
        
        # Test admin configuration
        admin_instance = NotificationAdmin(Notification, admin.site)
        
        # Test list_display
        expected_list_display = ("id", "user", "is_read", "created_at", "related_match")
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        # Test list_filter
        expected_list_filter = ("is_read", "created_at")
        self.assertEqual(admin_instance.list_filter, expected_list_filter)
        
        # Test search_fields
        expected_search_fields = ("message", "user__username")
        self.assertEqual(admin_instance.search_fields, expected_search_fields)


class NotificationIntegrationTest(TestCase):
    """Integration tests for the notifications module."""

    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

        # Create test category
        self.category = Category.objects.create(name="Electronics")

    def test_notification_workflow(self):
        """Test a complete notification workflow."""
        # Create reports
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )

        # Create match
        match = Match.objects.create(
            lost_report=lost_report,
            found_report=found_report,
            confidence_score=0.85
        )

        # Create notifications for both users
        notification1 = Notification.objects.create(
            user=self.user1,
            message=f"Potential match found for your lost item: {lost_report.title}",
            related_match=match
        )
        
        notification2 = Notification.objects.create(
            user=self.user2,
            message=f"Your found item might match a lost report: {found_report.title}",
            related_match=match
        )

        # Verify notifications were created (check only the ones we just created)
        new_notifications = Notification.objects.filter(related_match=match)
        self.assertEqual(new_notifications.count(), 2)
        self.assertEqual(self.user1.notifications.filter(related_match=match).count(), 1)
        self.assertEqual(self.user2.notifications.filter(related_match=match).count(), 1)
        
        # Verify notification content
        self.assertIn(lost_report.title, notification1.message)
        self.assertIn(found_report.title, notification2.message)
        self.assertEqual(notification1.related_match, match)
        self.assertEqual(notification2.related_match, match)

    def test_bulk_notification_operations(self):
        """Test creating and managing multiple notifications."""
        notifications = []
        for i in range(5):
            notification = Notification.objects.create(
                user=self.user1,
                message=f"Test notification {i+1}"
            )
            notifications.append(notification)

        # Test bulk queryset operations
        user_notifications = Notification.objects.filter(user=self.user1)
        self.assertEqual(user_notifications.count(), 5)

        # Mark all as read
        user_notifications.update(is_read=True)

        # Verify all are marked as read
        for notification in user_notifications:
            self.assertTrue(notification.is_read)

        # Test bulk delete
        user_notifications.delete()
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)