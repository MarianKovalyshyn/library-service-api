from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CreateUserViewTests(APITestCase):
    def test_create_user_successfully(self):
        url = reverse("user:create")
        payload = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_create_user_with_short_password(self):
        url = reverse("user:create")
        payload = {"email": "test@example.com", "password": "test"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            User.objects.filter(email="test@example.com").exists()
        )

    def test_create_user_with_invalid_email(self):
        url = reverse("user:create")
        payload = {"email": "testexample.com", "password": "testpass123"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="testexample.com").exists())


class ManageUserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        self.url = reverse("user:manage")
        self.client.force_authenticate(self.user)

    def test_retrieve_user_profile_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user_profile_authenticated(self):
        payload = {"email": "newemail@example.com"}
        response = self.client.patch(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")

    def test_retrieve_user_profile_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
