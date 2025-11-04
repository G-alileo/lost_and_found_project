from __future__ import annotations
from datetime import date
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from rest_framework import status
from rest_framework.test import APITestCase
from items.models import Category
from .models import Report


User = get_user_model()


class ReportTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
    
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            role="student"
        )
        self.admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="adminpass123",
            role="admin",
            is_staff=True
        )
        
        # Create test category
        self.category = Category.objects.create(name="Electronics")
        
        # Create base test report data
        test_date = date(2025, 11, 4)
        self.report_data = {
            "title": "Lost Laptop",
            "description": "MacBook Pro lost in library",
            "category": self.category.id,  # Use ID for API calls
            "report_type": Report.ReportType.LOST,
            "location": "University Library",
            "date_lost_found": test_date.isoformat()  # Use ISO format for API
        }
        
        # Data for direct model creation (used in setUp)
        self.model_data = {
            "title": "Lost Laptop",
            "description": "MacBook Pro lost in library",
            "category": self.category,  # Use actual instance for model
            "report_type": Report.ReportType.LOST,
            "location": "University Library",
            "date_lost_found": test_date
        }
        
        # API endpoints
        self.list_url = reverse("report-list")
        
    def tearDown(self):
        # Clean up after each test
        Report.objects.all().delete()
        super().tearDown()

    def test_create_report(self):
        # Test creating a new report
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, self.report_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(response.data["title"], self.report_data["title"])
        self.assertEqual(response.data["reported_by"], self.user.id)
        self.assertEqual(response.data["status"], Report.Status.PENDING)

    def test_create_report_with_image(self):
        """Test creating a report with an image attachment"""
        self.client.force_authenticate(user=self.user)
        # Create a minimal valid JPEG image (1x1 pixel)
        image_content = (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
            b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
            b'\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a'
            b'\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342'
            b'\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01'
            b'\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff'
            b'\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        )
        image = SimpleUploadedFile(
            name="test.jpg",
            content=image_content,
            content_type="image/jpeg"
        )
        # Build multipart form data
        data = {
            "title": "Lost Phone",
            "description": "iPhone lost in library",
            "category": self.category.id,
            "report_type": "lost",
            "location": "University Library",
            "date_lost_found": "2025-11-04",
            "image": image
        }
        response = self.client.post(self.list_url, data, format="multipart")
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data["image"])

    def test_list_reports(self):
        # Test listing all reports
        # Create a single test report for this test
        test_report = Report.objects.create(
            title="Test List Report",
            description="Test description for listing",
            category=self.category,
            report_type=Report.ReportType.LOST,
            location="Test Location",
            date_lost_found=date(2025, 11, 4),
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # Verify list serializer fields
        self.assertIn("title", response.data[0])
        self.assertIn("category", response.data[0])
        self.assertNotIn("description", response.data[0])  # Not in list serializer

    def test_retrieve_report(self):
        # Test retrieving a specific report
        # Create a test report for this test
        report = Report.objects.create(
            **self.model_data,
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        detail_url = reverse("report-detail", kwargs={"pk": report.pk})
        
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], report.title)
        # Verify detail serializer includes all fields
        self.assertIn("description", response.data)
        self.assertIn("status", response.data)

    def test_update_report_owner(self):
        # Test updating a report as owner
        # Create a test report for this test
        report = Report.objects.create(
            **self.model_data,
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        detail_url = reverse("report-detail", kwargs={"pk": report.pk})
        
        self.client.force_authenticate(user=self.user)
        updated_data = {
            "title": "Updated Title",
            "description": "Updated description"
        }
        response = self.client.patch(detail_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        report.refresh_from_db()
        self.assertEqual(report.title, "Updated Title")

    def test_update_report_non_owner(self):
        # Test updating a report as non-owner
        # Create a test report for this test
        report = Report.objects.create(
            **self.model_data,
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        detail_url = reverse("report-detail", kwargs={"pk": report.pk})
        
        other_user = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="pass123",
            role="student"
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(
            detail_url,
            {"title": "Unauthorized Update"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_report_owner(self):
        # Test deleting a report as owner
        # Create a test report for this test
        report = Report.objects.create(
            **self.model_data,
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        detail_url = reverse("report-detail", kwargs={"pk": report.pk})
        
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Report.objects.filter(pk=report.pk).exists())

    def test_filter_reports(self):
        """Test report filtering"""
        # Create a LOST report
        lost_report = Report.objects.create(
            title="Lost Laptop",
            description="MacBook Pro lost in library",
            category=self.category,
            report_type=Report.ReportType.LOST,
            location="University Library",
            date_lost_found=date(2025, 11, 4),
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        
        # Create a FOUND report
        found_report = Report.objects.create(
            title="Found Phone",
            description="iPhone found in cafeteria",
            category=self.category,
            report_type=Report.ReportType.FOUND,
            location="University Cafeteria",
            date_lost_found=date(2025, 11, 5),
            reported_by=self.user,
            status=Report.Status.PENDING
        )

        # Verify we have exactly 2 reports
        total_reports = Report.objects.count()
        self.assertEqual(total_reports, 2, f"Expected 2 reports, but found {total_reports}")

        # Test type filter - should only return lost reports
        response = self.client.get(f"{self.list_url}?type=lost")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, f"Expected 1 lost report, got {len(response.data)}")
        self.assertEqual(response.data[0]["report_type"], "lost")

        # Test category filter - should return both reports with same category
        response = self.client.get(f"{self.list_url}?category={self.category.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        # Test search - should only find the laptop report
        response = self.client.get(f"{self.list_url}?q=laptop")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Lost Laptop")

    def test_find_matches_endpoint(self):
        # Test the find_matches custom action
        # Create a test report for this test
        report = Report.objects.create(
            **self.model_data,
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        find_matches_url = reverse("report-find-matches", kwargs={"pk": report.pk})
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(find_matches_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["triggered"])

    def test_report_str_representation(self):
        # Test the string representation of Report model
        report = Report.objects.create(
            **self.model_data,
            reported_by=self.user,
            status=Report.Status.PENDING
        )
        self.assertEqual(
            str(report),
            f"{report.report_type}: {report.title}"
        )

    def test_report_type_choices(self):
        # Test Report type choices
        self.assertEqual(Report.ReportType.LOST, "lost")
        self.assertEqual(Report.ReportType.FOUND, "found")

    def test_report_status_choices(self):
        # Test Report status choices
        self.assertEqual(Report.Status.PENDING, "pending")
        self.assertEqual(Report.Status.MATCHED, "matched")
        self.assertEqual(Report.Status.CLAIMED, "claimed")
        self.assertEqual(Report.Status.UNCLAIMED, "unclaimed")
