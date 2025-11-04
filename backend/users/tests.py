from __future__ import annotations

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UsersAPITestCase(APITestCase):
	def setUp(self):
		# Common URLs
		self.register_url = reverse("auth-register")
		self.me_url = reverse("users-me")
		self.change_password_url = reverse("change-password")
		self.admin_login_url = reverse("admin-login")

	def test_registration_creates_user(self):
		payload = {
			"username": "jane",
			"email": "jane@example.com",
			"password": "Oldpass1!",
			"first_name": "Jane",
			"last_name": "Doe",
			"role": "student",
		}
		resp = self.client.post(self.register_url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.filter(username="jane").exists())
		user = User.objects.get(username="jane")
		self.assertNotEqual(user.password, payload["password"]) 
		self.assertTrue(user.check_password(payload["password"]))

	def test_registration_missing_fields_returns_400(self):
		payload = {"username": "bob", "email": "bob@example.com"}
		resp = self.client.post(self.register_url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

	def test_me_requires_authentication(self):
		resp = self.client.get(self.me_url)
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_me_get_returns_user_data(self):
		user = User.objects.create_user(username="alice", email="alice@example.com", password="Testpass1!", role="student")
		self.client.force_authenticate(user=user)
		resp = self.client.get(self.me_url)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertEqual(resp.data.get("username"), "alice")
		self.assertEqual(resp.data.get("email"), "alice@example.com")

	def test_me_put_updates_profile(self):
		user = User.objects.create_user(username="tom", email="tom@example.com", password="Testpass1!", role="student")
		self.client.force_authenticate(user=user)
		payload = {"first_name": "Tommy", "bio": "New bio here"}
		resp = self.client.put(self.me_url, payload, format="json")
		self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT))
		user.refresh_from_db()
		self.assertEqual(user.first_name, "Tommy")
		self.assertEqual(getattr(user, "bio", ""), "New bio here")

	def test_me_patch_updates_profile_partial(self):
		user = User.objects.create_user(username="lisa", email="lisa@example.com", password="Testpass1!", role="student")
		self.client.force_authenticate(user=user)
		payload = {"first_name": "LisaUpdated"}
		resp = self.client.patch(self.me_url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		user.refresh_from_db()
		self.assertEqual(user.first_name, "LisaUpdated")

	def test_change_password_success_and_failure(self):
		user = User.objects.create_user(username="paul", email="paul@example.com", password="Oldpass1!", role="student")
		self.client.force_authenticate(user=user)

		# Wrong current password
		payload_bad = {"current_password": "wrongpass", "new_password": "Newpass1!"}
		resp_bad = self.client.post(self.change_password_url, payload_bad, format="json")
		self.assertEqual(resp_bad.status_code, status.HTTP_400_BAD_REQUEST)

		# Correct current password and valid new password
		payload = {"current_password": "Oldpass1!", "new_password": "Newpass1!"}
		resp = self.client.post(self.change_password_url, payload, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		user.refresh_from_db()
		self.assertTrue(user.check_password("Newpass1!"))

	def test_admin_session_login(self):
		# Staff user should be able to login via admin-login
		staff = User.objects.create_user(username="staffuser", email="staff@example.com", password="Staffpass1!", role="staff")
		staff.is_staff = True
		staff.save()

		resp = self.client.post(self.admin_login_url, {"username": "staffuser", "password": "Staffpass1!"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertTrue(resp.data.get("success") is True)
		session = self.client.session
		self.assertIn("_auth_user_id", session)

	def test_admin_session_login_forbidden_for_non_admin(self):
		user = User.objects.create_user(username="regular", email="reg@example.com", password="Regpass1!", role="student")
		resp = self.client.post(self.admin_login_url, {"username": "regular", "password": "Regpass1!"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

