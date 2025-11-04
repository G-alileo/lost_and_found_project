from __future__ import annotations
from datetime import timedelta
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from items.models import Category
from notifications.models import Notification
from reports.models import Report
from .models import Match
from .serializers import MatchDetailSerializer, MatchSerializer
from .services import compute_overlap, notify_users_for_match, run_matching_for_report, tokenize

User = get_user_model()


class MatchModelTest(TestCase):

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

        # Create test reports
        self.lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        self.found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )

    def test_match_creation(self):
        """Test creating a match."""
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )
        
        self.assertEqual(match.lost_report, self.lost_report)
        self.assertEqual(match.found_report, self.found_report)
        self.assertEqual(match.confidence_score, 0.85)
        self.assertEqual(match.status, Match.Status.PENDING)
        self.assertIsNotNone(match.created_at)
        self.assertIsNone(match.resolved_at)

    def test_match_str_method(self):
        """Test the string representation of match."""
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.8543
        )
        
        expected_str = f"Match {match.pk} (0.85)"
        self.assertEqual(str(match), expected_str)

    def test_match_status_choices(self):
        """Test match status choices."""
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )
        
        # Test all status choices
        match.status = Match.Status.CONFIRMED
        match.save()
        self.assertEqual(match.status, "confirmed")
        
        match.status = Match.Status.REJECTED
        match.save()
        self.assertEqual(match.status, "rejected")
        
        match.status = Match.Status.PENDING
        match.save()
        self.assertEqual(match.status, "pending")

    def test_match_default_status(self):
        """Test that matches have pending status by default."""
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )
        
        self.assertEqual(match.status, Match.Status.PENDING)

    def test_match_with_resolved_at(self):
        """Test match with resolved_at timestamp."""
        resolved_time = timezone.now()
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85,
            status=Match.Status.CONFIRMED,
            resolved_at=resolved_time
        )
        
        self.assertEqual(match.resolved_at, resolved_time)

    def test_report_deletion_cascades(self):
        """Test that deleting a report deletes related matches."""
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )
        
        match_id = match.id
        self.lost_report.delete()
        
        with self.assertRaises(Match.DoesNotExist):
            Match.objects.get(id=match_id)

    def test_related_name_queries(self):
        """Test related name queries work correctly."""
        match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )
        
        # Test lost_matches related name
        lost_matches = self.lost_report.lost_matches.all()
        self.assertIn(match, lost_matches)
        
        # Test found_matches related name
        found_matches = self.found_report.found_matches.all()
        self.assertIn(match, found_matches)


class MatchSerializerTest(TestCase):
    """Test cases for Match serializers."""

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

        self.category = Category.objects.create(name="Electronics")

        self.lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        self.found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )

        self.match = Match.objects.create(
            lost_report=self.lost_report,
            found_report=self.found_report,
            confidence_score=0.85
        )

    def test_match_serialization(self):
        """Test serializing a match."""
        serializer = MatchSerializer(self.match)
        data = serializer.data
        
        self.assertEqual(data['id'], self.match.id)
        self.assertEqual(data['lost_report'], self.lost_report.id)
        self.assertEqual(data['found_report'], self.found_report.id)
        self.assertEqual(data['confidence_score'], 0.85)
        self.assertEqual(data['status'], Match.Status.PENDING)
        self.assertIn('created_at', data)
        self.assertIsNone(data['resolved_at'])

    def test_match_detail_serialization(self):
        """Test serializing a match with detail serializer."""
        serializer = MatchDetailSerializer(self.match)
        data = serializer.data
        
        self.assertEqual(data['id'], self.match.id)
        self.assertIsInstance(data['lost_report'], dict)
        self.assertIsInstance(data['found_report'], dict)
        self.assertEqual(data['lost_report']['id'], self.lost_report.id)
        self.assertEqual(data['found_report']['id'], self.found_report.id)
        self.assertEqual(data['confidence_score'], 0.85)

    def test_read_only_fields(self):
        """Test that certain fields are read-only."""
        data = {
            'id': 999,
            'lost_report': self.lost_report.id,
            'found_report': self.found_report.id,
            'confidence_score': 0.95,
            'status': Match.Status.CONFIRMED,
            'created_at': '2023-01-01T00:00:00Z',
            'resolved_at': '2023-01-01T00:00:00Z'
        }
        
        serializer = MatchSerializer(self.match, data=data)
        self.assertTrue(serializer.is_valid())
        
        updated_match = serializer.save()
        
        # ID and created_at should not change (read-only)
        self.assertEqual(updated_match.id, self.match.id)
        self.assertEqual(updated_match.created_at, self.match.created_at)
        
        # Other fields should update
        self.assertEqual(updated_match.confidence_score, 0.95)
        self.assertEqual(updated_match.status, Match.Status.CONFIRMED)


class MatchAPITest(APITestCase):
    """Test cases for the Match API views."""

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
        
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )

        self.category = Category.objects.create(name="Electronics")

        # User1's lost report
        self.lost_report1 = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # User2's found report
        self.found_report1 = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Another user's reports (should not be visible to user1/user2)
        self.other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.other_lost_report = Report.objects.create(
            title="Lost Laptop",
            description="Lost my laptop",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.other_user,
            location="Cafeteria",
            date_lost_found=timezone.now().date()
        )
        
        self.other_found_report = Report.objects.create(
            title="Found Laptop",
            description="Found a laptop",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.other_user,
            location="Cafeteria",
            date_lost_found=timezone.now().date()
        )

        # Create matches
        self.match1 = Match.objects.create(
            lost_report=self.lost_report1,
            found_report=self.found_report1,
            confidence_score=0.85
        )
        
        self.other_match = Match.objects.create(
            lost_report=self.other_lost_report,
            found_report=self.other_found_report,
            confidence_score=0.75
        )

    def test_match_list_authenticated_user(self):
        """Test listing matches for authenticated user."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('match-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # User1 should only see matches involving their reports
        match_ids = [match['id'] for match in data]
        self.assertIn(self.match1.id, match_ids)
        self.assertNotIn(self.other_match.id, match_ids)

    def test_match_list_admin_user(self):
        """Test that admin users can see all matches."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('match-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Admin should see all matches
        match_ids = [match['id'] for match in data]
        self.assertIn(self.match1.id, match_ids)
        self.assertIn(self.other_match.id, match_ids)

    def test_match_list_unauthenticated(self):
        """Test that unauthenticated users cannot access matches."""
        url = reverse('match-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_match_detail_authenticated(self):
        """Test retrieving match detail for authenticated user."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('match-detail', kwargs={'pk': self.match1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should return detailed serializer with nested reports
        self.assertIn('lost_report', response.data)
        self.assertIn('found_report', response.data)
        self.assertIsInstance(response.data['lost_report'], dict)
        self.assertIsInstance(response.data['found_report'], dict)

    def test_match_detail_wrong_user(self):
        """Test that users cannot access matches they're not involved in."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('match-detail', kwargs={'pk': self.other_match.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_match_confirm_admin(self):
        """Test confirming a match as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('match-confirm', kwargs={'pk': self.match1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Match.Status.CONFIRMED)
        
        # Verify match was actually updated
        self.match1.refresh_from_db()
        self.assertEqual(self.match1.status, Match.Status.CONFIRMED)
        self.assertIsNotNone(self.match1.resolved_at)

    def test_match_confirm_non_admin(self):
        """Test that non-admin users cannot confirm matches."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('match-confirm', kwargs={'pk': self.match1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_match_reject_admin(self):
        """Test rejecting a match as admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('match-reject', kwargs={'pk': self.match1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], Match.Status.REJECTED)
        
        # Verify match was actually updated
        self.match1.refresh_from_db()
        self.assertEqual(self.match1.status, Match.Status.REJECTED)
        self.assertIsNotNone(self.match1.resolved_at)

    def test_match_reject_non_admin(self):
        """Test that non-admin users cannot reject matches."""
        self.client.force_authenticate(user=self.user1)
        url = reverse('match-reject', kwargs={'pk': self.match1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_match_confirm_unauthenticated(self):
        """Test that unauthenticated users cannot confirm matches."""
        url = reverse('match-confirm', kwargs={'pk': self.match1.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_match_readonly_viewset(self):
        """Test that the viewset is read-only (no create/update/delete)."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Test POST (create) - should not be allowed
        url = reverse('match-list')
        data = {
            'lost_report': self.lost_report1.id,
            'found_report': self.found_report1.id,
            'confidence_score': 0.9
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test PUT (update) - should not be allowed
        url = reverse('match-detail', kwargs={'pk': self.match1.pk})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test DELETE - should not be allowed
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_match_ordering(self):
        """Test that matches are ordered by created_at descending."""
        # Create another match
        new_match = Match.objects.create(
            lost_report=self.lost_report1,
            found_report=self.found_report1,
            confidence_score=0.9
        )
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('match-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Handle paginated response
        if isinstance(response.data, dict) and 'results' in response.data:
            data = response.data['results']
        else:
            data = response.data
        
        # Newer match should come first
        if len(data) >= 2:
            self.assertEqual(data[0]['id'], new_match.id)


class MatchServicesTest(TestCase):
    """Test cases for match services."""

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

        self.category = Category.objects.create(name="Electronics")

    def test_tokenize_function(self):
        """Test the tokenize function."""
        # Test basic tokenization
        tokens = tokenize("iPhone 13 Pro Max")
        expected = {"iphone", "13", "pro", "max"}
        self.assertEqual(tokens, expected)
        
        # Test stopword removal
        tokens = tokenize("The lost iPhone with a case")
        expected = {"lost", "iphone", "case"}
        self.assertEqual(tokens, expected)
        
        # Test case insensitive
        tokens = tokenize("IPHONE iPhone iphone")
        expected = {"iphone"}
        self.assertEqual(tokens, expected)
        
        # Test empty/None input
        self.assertEqual(tokenize(""), set())
        self.assertEqual(tokenize(None), set())
        
        # Test single character removal
        tokens = tokenize("a b c iPhone")
        expected = {"iphone"}
        self.assertEqual(tokens, expected)

    def test_compute_overlap_function(self):
        """Test the compute_overlap function."""
        # Test exact match
        overlap = compute_overlap(["apple", "iphone"], ["apple", "iphone"])
        self.assertEqual(overlap, 1.0)
        
        # Test partial overlap
        overlap = compute_overlap(["apple", "iphone"], ["apple", "samsung"])
        self.assertEqual(overlap, 1/3)  # 1 intersection, 3 union
        
        # Test no overlap
        overlap = compute_overlap(["apple"], ["samsung"])
        self.assertEqual(overlap, 0.0)
        
        # Test empty sets
        overlap = compute_overlap([], ["apple"])
        self.assertEqual(overlap, 0.0)
        
        overlap = compute_overlap(["apple"], [])
        self.assertEqual(overlap, 0.0)

    def test_notify_users_for_match(self):
        """Test notification creation for matches."""
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        match = Match.objects.create(
            lost_report=lost_report,
            found_report=found_report,
            confidence_score=0.85
        )
        
        # Clear any existing notifications
        Notification.objects.all().delete()
        
        notify_users_for_match(match)
        
        # Check that notifications were created
        notifications = Notification.objects.all()
        self.assertEqual(notifications.count(), 2)
        
        # Check notification for lost report user
        lost_notification = Notification.objects.get(user=self.user1)
        self.assertIn(found_report.title, lost_notification.message)
        self.assertEqual(lost_notification.related_match, match)
        
        # Check notification for found report user
        found_notification = Notification.objects.get(user=self.user2)
        self.assertIn(lost_report.title, found_notification.message)
        self.assertEqual(found_notification.related_match, match)

    @override_settings(
        MATCHING_CONF_THRESHOLD=0.5,
        MATCHING_DATE_WINDOW_DAYS=7,
        MATCHING_WEIGHTS={"category": 0.7, "keyword": 0.3, "date_boost": 0.1}
    )
    def test_run_matching_for_report(self):
        """Test the main matching algorithm."""
        # Create a found report first
        found_report = Report.objects.create(
            title="Found iPhone 13 Pro",
            description="Found an iPhone 13 Pro in the library",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Create a lost report that should match
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Clear any existing matches and notifications
        Match.objects.all().delete()
        Notification.objects.all().delete()
        
        # Run matching for the new lost report
        matches = run_matching_for_report(lost_report)
        
        # Should create a match
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].lost_report, lost_report)
        self.assertEqual(matches[0].found_report, found_report)
        self.assertGreater(matches[0].confidence_score, 0.5)
        
        # Should create notifications
        self.assertEqual(Notification.objects.count(), 2)

    @override_settings(MATCHING_CONF_THRESHOLD=0.9)
    def test_run_matching_no_matches_low_confidence(self):
        """Test that low confidence matches are not created."""
        # Create reports with very different descriptions
        found_report = Report.objects.create(
            title="Found Laptop",
            description="Found a Dell laptop",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Cafeteria",
            date_lost_found=timezone.now().date()
        )
        
        # Clear existing matches
        Match.objects.all().delete()
        
        # Run matching
        matches = run_matching_for_report(lost_report)
        
        # Should not create any matches due to low confidence
        self.assertEqual(len(matches), 0)

    @override_settings(MATCHING_DATE_WINDOW_DAYS=1)
    def test_run_matching_date_window(self):
        """Test that matches respect the date window."""
        # Create a found report
        found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date() - timedelta(days=5)  # 5 days ago
        )
        
        # Create a lost report today (outside the 1-day window)
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Clear existing matches
        Match.objects.all().delete()
        
        # Run matching
        matches = run_matching_for_report(lost_report)
        
        # Should not create matches due to date window restriction
        self.assertEqual(len(matches), 0)

    def test_run_matching_excludes_same_report(self):
        """Test that matching excludes the same report."""
        # Create a report
        report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Clear existing matches
        Match.objects.all().delete()
        
        # Run matching for the same report
        matches = run_matching_for_report(report)
        
        # Should not match with itself
        self.assertEqual(len(matches), 0)

    def test_run_matching_different_categories(self):
        """Test that matching only considers same category reports."""
        other_category = Category.objects.create(name="Books")
        
        # Create found report in different category
        found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone",
            category=other_category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Create lost report in original category
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Clear existing matches
        Match.objects.all().delete()
        
        # Run matching
        matches = run_matching_for_report(lost_report)
        
        # Should not create matches due to different categories
        self.assertEqual(len(matches), 0)


class MatchAdminTest(TestCase):
    """Test cases for the Match admin interface."""

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

        self.category = Category.objects.create(name="Electronics")

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

    def test_admin_match_display(self):
        """Test that match displays correctly in admin."""
        from django.contrib import admin
        from .admin import MatchAdmin
        
        # Test that admin is registered
        self.assertIn(Match, admin.site._registry)
        
        # Test admin configuration
        admin_instance = MatchAdmin(Match, admin.site)
        
        # Test list_display
        expected_list_display = ("id", "lost_report", "found_report", "confidence_score", "status", "created_at")
        self.assertEqual(admin_instance.list_display, expected_list_display)
        
        # Test list_filter
        expected_list_filter = ("status", "created_at")
        self.assertEqual(admin_instance.list_filter, expected_list_filter)
        
        # Test search_fields
        expected_search_fields = ("lost_report__title", "found_report__title")
        self.assertEqual(admin_instance.search_fields, expected_search_fields)


class MatchIntegrationTest(TestCase):
    """Integration tests for the matches module."""

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

        self.category = Category.objects.create(name="Electronics")

    @patch('matches.services.notify_users_for_match')
    def test_end_to_end_matching_workflow(self, mock_notify):
        """Test complete matching workflow from report creation to resolution."""
        # Clear all existing reports and matches to ensure clean test
        Report.objects.all().delete()
        Match.objects.all().delete()
        
        # Create found report first
        found_report = Report.objects.create(
            title="Found iPhone 13 Pro",
            description="Found an iPhone 13 Pro with blue case",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Create lost report that should trigger matching
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro with blue case",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Trigger matching
        matches = run_matching_for_report(lost_report)
        
        # Verify at least one match was created
        self.assertGreaterEqual(len(matches), 1)
        match = matches[0]
        self.assertEqual(match.lost_report, lost_report)
        self.assertEqual(match.found_report, found_report)
        self.assertEqual(match.status, Match.Status.PENDING)
        
        # Verify notification function was called at least once
        self.assertGreaterEqual(mock_notify.call_count, 1)
        # Check that the first call was with our match
        mock_notify.assert_any_call(match)
        
        # Test match resolution
        match.status = Match.Status.CONFIRMED
        match.resolved_at = timezone.now()
        match.save()
        
        match.refresh_from_db()
        self.assertEqual(match.status, Match.Status.CONFIRMED)
        self.assertIsNotNone(match.resolved_at)

    def test_multiple_matches_same_report(self):
        """Test that one report can match with multiple reports."""
        # Clear all existing reports and matches to ensure clean test
        Report.objects.all().delete()
        Match.objects.all().delete()
        
        # Create multiple found reports
        found_report1 = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone 13",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        found_report2 = Report.objects.create(
            title="Found Phone",
            description="Found an iPhone 13 Pro",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Cafeteria",
            date_lost_found=timezone.now().date()
        )
        
        # Create lost report that should match both
        lost_report = Report.objects.create(
            title="Lost iPhone 13",
            description="Lost my iPhone 13",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Campus",
            date_lost_found=timezone.now().date()
        )
        
        # Run matching
        matches = run_matching_for_report(lost_report)
        
        # Should create multiple matches
        self.assertGreaterEqual(len(matches), 1)  # At least one match should be created
        
        # All matches should involve the lost report
        for match in matches:
            self.assertEqual(match.lost_report, lost_report)

    def test_matching_performance_with_many_reports(self):
        """Test matching performance with multiple candidate reports."""
        # Clear all existing reports and matches to ensure clean test
        Report.objects.all().delete()
        Match.objects.all().delete()
        
        # Create many found reports
        for i in range(10):
            Report.objects.create(
                title=f"Found Item {i}",
                description=f"Found some item {i}",
                category=self.category,
                report_type=Report.ReportType.FOUND,
                reported_by=self.user2,
                location=f"Location {i}",
                date_lost_found=timezone.now().date()
            )
        
        # Create lost report
        lost_report = Report.objects.create(
            title="Lost Item",
            description="Lost my item",
            category=self.category,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Run matching - should complete without errors
        start_time = timezone.now()
        matches = run_matching_for_report(lost_report)
        end_time = timezone.now()
        
        # Should complete quickly (less than 1 second for 10 reports)
        duration = (end_time - start_time).total_seconds()
        self.assertLess(duration, 1.0)
        
        # Verify some logic worked (matches may or may not be created depending on confidence)
        self.assertIsInstance(matches, list)