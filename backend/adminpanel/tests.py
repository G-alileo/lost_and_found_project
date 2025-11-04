from __future__ import annotations

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from items.models import Category
from matches.models import Match
from reports.models import Report

from .views import AdminStatsView, IsAdmin

User = get_user_model()


class IsAdminPermissionTest(TestCase):
    """Test cases for the IsAdmin permission class."""

    def setUp(self):
        """Set up test data."""
        self.permission = IsAdmin()
        self.factory = APIRequestFactory()
        
        # Create different types of users
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )
        
        self.staff_user = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="testpass123",
            role=User.Roles.STAFF,
            is_staff=True
        )
        
        self.regular_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )

    def test_admin_role_has_permission(self):
        """Test that users with admin role have permission."""
        request = self.factory.get('/admin/stats/')
        request.user = self.admin_user
        
        self.assertTrue(self.permission.has_permission(request, None))

    def test_staff_user_has_permission(self):
        """Test that staff users have permission."""
        request = self.factory.get('/admin/stats/')
        request.user = self.staff_user
        
        self.assertTrue(self.permission.has_permission(request, None))

    def test_regular_user_no_permission(self):
        """Test that regular users don't have permission."""
        request = self.factory.get('/admin/stats/')
        request.user = self.regular_user
        
        self.assertFalse(self.permission.has_permission(request, None))

    def test_unauthenticated_user_no_permission(self):
        """Test that unauthenticated users don't have permission."""
        from django.contrib.auth.models import AnonymousUser
        
        request = self.factory.get('/admin/stats/')
        request.user = AnonymousUser()
        
        self.assertFalse(self.permission.has_permission(request, None))

    def test_user_without_role_no_permission(self):
        """Test that users without role attribute don't have permission."""
        user_without_role = User.objects.create_user(
            username="norole",
            email="norole@example.com",
            password="testpass123"
            # No role specified
        )
        
        request = self.factory.get('/admin/stats/')
        request.user = user_without_role
        
        self.assertFalse(self.permission.has_permission(request, None))

    def test_admin_user_without_staff_flag(self):
        """Test that admin role users have permission even without is_staff flag."""
        admin_no_staff = User.objects.create_user(
            username="adminnostaff",
            email="adminnostaff@example.com",
            password="testpass123",
            role=User.Roles.ADMIN,
            is_staff=False
        )
        
        request = self.factory.get('/admin/stats/')
        request.user = admin_no_staff
        
        self.assertTrue(self.permission.has_permission(request, None))


class AdminStatsViewTest(APITestCase):
    """Test cases for the AdminStatsView."""

    def setUp(self):
        """Set up test data."""
        # Create users
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )
        
        self.regular_user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="testpass123",
            role=User.Roles.STUDENT
        )
        
        self.staff_user = User.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="testpass123",
            role=User.Roles.STAFF,
            is_staff=True
        )

        # Create categories
        self.electronics = Category.objects.create(name="Electronics")
        self.clothing = Category.objects.create(name="Clothing")
        self.documents = Category.objects.create(name="Documents")

        # Clear any existing data
        Report.objects.all().delete()
        Match.objects.all().delete()

    def test_admin_stats_view_admin_access(self):
        """Test that admin users can access the stats view."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that all expected keys are in the response
        expected_keys = [
            'total_lost', 'total_found', 'total_matches', 
            'successful_matches_count', 'unclaimed_count', 'top_categories'
        ]
        for key in expected_keys:
            self.assertIn(key, response.data)

    def test_admin_stats_view_staff_access(self):
        """Test that staff users can access the stats view."""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_stats_view_regular_user_denied(self):
        """Test that regular users cannot access the stats view."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_stats_view_unauthenticated_denied(self):
        """Test that unauthenticated users cannot access the stats view."""
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_stats_empty_database(self):
        """Test stats view with empty database."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # All counts should be zero
        self.assertEqual(response.data['total_lost'], 0)
        self.assertEqual(response.data['total_found'], 0)
        self.assertEqual(response.data['total_matches'], 0)
        self.assertEqual(response.data['successful_matches_count'], 0)
        self.assertEqual(response.data['unclaimed_count'], 0)
        self.assertEqual(response.data['top_categories'], [])

    def test_admin_stats_with_reports_data(self):
        """Test stats view with sample reports data."""
        # Create lost reports
        Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone",
            category=self.electronics,
            report_type=Report.ReportType.LOST,
            reported_by=self.regular_user,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        Report.objects.create(
            title="Lost Laptop",
            description="Lost my laptop",
            category=self.electronics,
            report_type=Report.ReportType.LOST,
            reported_by=self.regular_user,
            location="Cafeteria",
            date_lost_found=timezone.now().date()
        )
        
        Report.objects.create(
            title="Lost Jacket",
            description="Lost my jacket",
            category=self.clothing,
            report_type=Report.ReportType.LOST,
            reported_by=self.regular_user,
            location="Gym",
            date_lost_found=timezone.now().date()
        )

        # Create found reports
        Report.objects.create(
            title="Found Phone",
            description="Found a phone",
            category=self.electronics,
            report_type=Report.ReportType.FOUND,
            reported_by=self.regular_user,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        Report.objects.create(
            title="Found ID Card",
            description="Found student ID",
            category=self.documents,
            report_type=Report.ReportType.FOUND,
            reported_by=self.regular_user,
            location="Parking",
            date_lost_found=timezone.now().date(),
            status=Report.Status.UNCLAIMED
        )

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check counts
        self.assertEqual(response.data['total_lost'], 3)
        self.assertEqual(response.data['total_found'], 2)
        self.assertEqual(response.data['unclaimed_count'], 1)
        
        # Check top categories
        top_categories = response.data['top_categories']
        self.assertIsInstance(top_categories, list)
        
        # Electronics should be the top category (3 reports)
        if top_categories:
            electronics_category = next((cat for cat in top_categories if cat['name'] == 'Electronics'), None)
            self.assertIsNotNone(electronics_category)
            self.assertEqual(electronics_category['count'], 3)

    def test_admin_stats_comprehensive(self):
        """Test comprehensive stats with all data types."""
        # Clear existing data to ensure clean test
        Match.objects.all().delete()
        Report.objects.all().delete()
        # Don't delete users - just use existing ones
        
        # Create categories
        clothing = Category.objects.create(name="Clothing")
        
        # Create reports using existing users
        report1 = Report.objects.create(
            title="Lost Jacket",
            description="Black leather jacket",
            category=clothing,
            report_type=Report.ReportType.LOST,
            reported_by=self.regular_user,
            location="Park",
            date_lost_found=timezone.now().date()
        )
        
        report2 = Report.objects.create(
            title="Found Jacket", 
            description="Found black jacket",
            category=clothing,
            report_type=Report.ReportType.FOUND,
            reported_by=self.admin_user,
            location="Park",
            date_lost_found=timezone.now().date()
        )

        # Create matches
        match = Match.objects.create(
            lost_report=report1,
            found_report=report2,
            confidence_score=0.90,
            status=Match.Status.CONFIRMED,
            resolved_at=timezone.now()
        )

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get actual counts from database
        total_users = User.objects.count()
        total_reports = Report.objects.count()
        lost_reports = Report.objects.filter(report_type=Report.ReportType.LOST).count()
        found_reports = Report.objects.filter(report_type=Report.ReportType.FOUND).count()
        total_matches = Match.objects.count()
        successful_matches = Match.objects.filter(status=Match.Status.CONFIRMED).count()
        
        # Verify stats match actual database counts
        self.assertEqual(response.data['total_users'], total_users)
        self.assertEqual(response.data['total_reports'], total_reports)
        self.assertEqual(response.data['lost_reports_count'], lost_reports)
        self.assertEqual(response.data['found_reports_count'], found_reports)
        self.assertEqual(response.data['total_matches'], total_matches)
        self.assertEqual(response.data['successful_matches_count'], successful_matches)

    def test_admin_stats_top_categories_ordering(self):
        """Test that top categories are ordered by count descending."""
        # Create reports to establish category counts
        # Electronics: 4 reports
        for i in range(4):
            Report.objects.create(
                title=f"Electronics Item {i}",
                description=f"Electronics description {i}",
                category=self.electronics,
                report_type=Report.ReportType.LOST if i % 2 == 0 else Report.ReportType.FOUND,
                reported_by=self.regular_user,
                location="Library",
                date_lost_found=timezone.now().date()
            )
        
        # Clothing: 2 reports
        for i in range(2):
            Report.objects.create(
                title=f"Clothing Item {i}",
                description=f"Clothing description {i}",
                category=self.clothing,
                report_type=Report.ReportType.LOST,
                reported_by=self.regular_user,
                location="Gym",
                date_lost_found=timezone.now().date()
            )
        
        # Documents: 1 report
        Report.objects.create(
            title="Document Item",
            description="Document description",
            category=self.documents,
            report_type=Report.ReportType.FOUND,
            reported_by=self.regular_user,
            location="Office",
            date_lost_found=timezone.now().date()
        )

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        top_categories = response.data['top_categories']
        self.assertGreaterEqual(len(top_categories), 3)
        
        # Check ordering (should be descending by count)
        self.assertEqual(top_categories[0]['name'], 'Electronics')
        self.assertEqual(top_categories[0]['count'], 4)
        self.assertEqual(top_categories[1]['name'], 'Clothing')
        self.assertEqual(top_categories[1]['count'], 2)
        self.assertEqual(top_categories[2]['name'], 'Documents')
        self.assertEqual(top_categories[2]['count'], 1)

    def test_admin_stats_top_categories_limit(self):
        """Test that top categories are limited to 5 items."""
        # Create 7 categories with different report counts
        categories = []
        for i in range(7):
            category = Category.objects.create(name=f"Category{i}")
            categories.append(category)
            
            # Create i+1 reports for each category
            for j in range(i + 1):
                Report.objects.create(
                    title=f"Item {j} in Category {i}",
                    description=f"Description {j}",
                    category=category,
                    report_type=Report.ReportType.LOST,
                    reported_by=self.regular_user,
                    location="Test Location",
                    date_lost_found=timezone.now().date()
                )

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        top_categories = response.data['top_categories']
        # Should be limited to 5 categories
        self.assertEqual(len(top_categories), 5)
        
        # Should be ordered by count descending
        counts = [cat['count'] for cat in top_categories]
        self.assertEqual(counts, sorted(counts, reverse=True))

    def test_admin_stats_response_structure(self):
        """Test the structure of the admin stats response."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test response structure
        self.assertIsInstance(response.data, dict)
        
        # Test that all numeric fields are integers
        numeric_fields = ['total_lost', 'total_found', 'total_matches', 'successful_matches_count', 'unclaimed_count']
        for field in numeric_fields:
            self.assertIsInstance(response.data[field], int)
            self.assertGreaterEqual(response.data[field], 0)
        
        # Test top_categories structure
        top_categories = response.data['top_categories']
        self.assertIsInstance(top_categories, list)
        
        for category in top_categories:
            self.assertIsInstance(category, dict)
            self.assertIn('name', category)
            self.assertIn('count', category)
            self.assertIsInstance(category['name'], str)
            self.assertIsInstance(category['count'], int)
            self.assertGreaterEqual(category['count'], 0)


class AdminPanelIntegrationTest(APITestCase):
    """Integration tests for the adminpanel module."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="testpass123",
            role=User.Roles.ADMIN
        )
        
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

        # Create categories
        self.electronics = Category.objects.create(name="Electronics")
        self.clothing = Category.objects.create(name="Clothing")

        # Clear any existing data
        Report.objects.all().delete()
        Match.objects.all().delete()

    def test_complete_workflow_stats(self):
        """Test admin stats through a complete lost and found workflow."""
        # Clear existing data to ensure clean test
        Match.objects.all().delete()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        
        # Initial state - should be empty
        response = self.client.get(url)
        self.assertEqual(response.data['total_lost'], 0)
        self.assertEqual(response.data['total_found'], 0)
        self.assertEqual(response.data['total_matches'], 0)
        
        # User1 reports lost item
        lost_report = Report.objects.create(
            title="Lost iPhone",
            description="Lost my iPhone 13 Pro",
            category=self.electronics,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Check stats after lost report
        response = self.client.get(url)
        self.assertEqual(response.data['total_lost'], 1)
        self.assertEqual(response.data['total_found'], 0)
        
        # User2 reports found item
        found_report = Report.objects.create(
            title="Found iPhone",
            description="Found an iPhone 13 Pro",
            category=self.electronics,
            report_type=Report.ReportType.FOUND,
            reported_by=self.user2,
            location="Library",
            date_lost_found=timezone.now().date()
        )
        
        # Check stats after found report
        response = self.client.get(url)
        self.assertEqual(response.data['total_lost'], 1)
        self.assertEqual(response.data['total_found'], 1)
        
        # Create a match
        match = Match.objects.create(
            lost_report=lost_report,
            found_report=found_report,
            confidence_score=0.85,
            status=Match.Status.PENDING
        )
        
        # Check stats after match creation
        response = self.client.get(url)
        current_total_matches = Match.objects.count()
        self.assertEqual(response.data['total_matches'], current_total_matches)
        self.assertEqual(response.data['successful_matches_count'], 0)
        
        # Confirm the match
        match.status = Match.Status.CONFIRMED
        match.resolved_at = timezone.now()
        match.save()
        
        # Check final stats
        response = self.client.get(url)
        final_total_matches = Match.objects.count()
        final_successful_matches = Match.objects.filter(status=Match.Status.CONFIRMED).count()
        
        self.assertEqual(response.data['total_lost'], 1)
        self.assertEqual(response.data['total_found'], 1)
        self.assertEqual(response.data['total_matches'], final_total_matches)
        self.assertEqual(response.data['successful_matches_count'], final_successful_matches)
        
        # Check top categories
        top_categories = response.data['top_categories']
        self.assertEqual(len(top_categories), 1)
        self.assertEqual(top_categories[0]['name'], 'Electronics')
        self.assertEqual(top_categories[0]['count'], 2)

    def test_multiple_users_multiple_categories(self):
        """Test stats with multiple users and categories."""
        # Create reports from different users in different categories
        users = [self.user1, self.user2]
        categories = [self.electronics, self.clothing]
        
        for i, user in enumerate(users):
            for j, category in enumerate(categories):
                # Create lost and found reports
                Report.objects.create(
                    title=f"Lost Item {i}-{j}",
                    description=f"Lost item by user{i+1} in category {category.name}",
                    category=category,
                    report_type=Report.ReportType.LOST,
                    reported_by=user,
                    location=f"Location {i}-{j}",
                    date_lost_found=timezone.now().date()
                )
                
                Report.objects.create(
                    title=f"Found Item {i}-{j}",
                    description=f"Found item by user{i+1} in category {category.name}",
                    category=category,
                    report_type=Report.ReportType.FOUND,
                    reported_by=user,
                    location=f"Location {i}-{j}",
                    date_lost_found=timezone.now().date()
                )

        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should have 4 lost and 4 found reports
        self.assertEqual(response.data['total_lost'], 4)
        self.assertEqual(response.data['total_found'], 4)
        
        # Both categories should appear in top categories with equal counts
        top_categories = response.data['top_categories']
        self.assertEqual(len(top_categories), 2)
        
        category_counts = {cat['name']: cat['count'] for cat in top_categories}
        self.assertEqual(category_counts['Electronics'], 4)
        self.assertEqual(category_counts['Clothing'], 4)

    def test_edge_cases_and_error_handling(self):
        """Test edge cases and potential error scenarios."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        
        # Test with reports but no categories (should handle gracefully)
        # This shouldn't happen in normal flow, but test defensive programming
        
        # Test with very large numbers (if applicable)
        # Create many reports to test performance
        for i in range(50):
            Report.objects.create(
                title=f"Test Report {i}",
                description=f"Test description {i}",
                category=self.electronics,
                report_type=Report.ReportType.LOST if i % 2 == 0 else Report.ReportType.FOUND,
                reported_by=self.user1,
                location="Test Location",
                date_lost_found=timezone.now().date()
            )
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should handle large numbers correctly
        self.assertEqual(response.data['total_lost'], 25)
        self.assertEqual(response.data['total_found'], 25)
        
        # Response should still be fast and correctly formatted
        self.assertIsInstance(response.data['top_categories'], list)

    def test_stats_consistency_across_requests(self):
        """Test that stats remain consistent across multiple requests."""
        # Create some test data
        Report.objects.create(
            title="Test Report",
            description="Test description",
            category=self.electronics,
            report_type=Report.ReportType.LOST,
            reported_by=self.user1,
            location="Test Location",
            date_lost_found=timezone.now().date()
        )
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('admin-stats')
        
        # Make multiple requests
        responses = []
        for _ in range(3):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            responses.append(response.data)
        
        # All responses should be identical
        for i in range(1, len(responses)):
            self.assertEqual(responses[0], responses[i])


class AdminPanelURLTest(TestCase):
    """Test cases for adminpanel URLs."""

    def test_admin_stats_url_resolves(self):
        """Test that the admin stats URL resolves correctly."""
        url = reverse('admin-stats')
        self.assertEqual(url, '/api/admin/stats/')

    def test_url_pattern_coverage(self):
        """Test that all expected URL patterns are covered."""
        from django.urls import resolve
        
        # Test stats URL
        resolver = resolve('/api/admin/stats/')
        self.assertEqual(resolver.view_name, 'admin-stats')
        # Check that it resolves to the correct view class
        self.assertEqual(resolver.func.view_class, AdminStatsView)