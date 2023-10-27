from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer, BorrowingDetailSerializer
)


BORROWING_URL = reverse("borrowing-service:borrowing-list")


def book(**params):
    defaults = {
        "title": "book",
        "author": "author",
        "inventory": 10,
        "daily_fee": 0.25,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


def detail_url(borrowing_id: int):
    return reverse("borrowing-service:borrowing-detail", args=[borrowing_id])


class UnauthenticatedBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "password123",
        )
        self.client.force_authenticate(self.user)
        self.book1 = book()
        self.book2 = book(title="book2")
        self.serializer = BookSerializer(self.book1)
        self.borrowing = Borrowing.objects.create(
            book=self.book1,
            user=self.user,
            expected_return_date=timezone.now() + timedelta(days=1),
        )

    def test_list_borrowings(self):
        response = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingSerializer(borrowings, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_borrowings_authenticated(self):
        response = self.client.get(detail_url(self.borrowing.id))

        borrowing = Borrowing.objects.get(id=self.borrowing.id)
        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class TestFilter(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "admin1234",
        )

        self.client.force_authenticate(self.user)
        self.book1 = book()
        self.book2 = book(title="book2")
        self.serializer1 = BookSerializer(self.book1)
        self.serializer2 = BookSerializer(self.book2)
        self.borrowing1 = Borrowing.objects.create(
            book=self.book1,
            user=self.user,
            expected_return_date=timezone.now() + timedelta(days=1),
        )
        self.borrowing2 = Borrowing.objects.create(
            book=self.book2,
            user=self.user,
            actual_return_date=timezone.now(),
            expected_return_date=timezone.now() + timedelta(days=1),
        )

    def test_borrowings_filter(self):
        res_user = self.client.get(
            BORROWING_URL,
            {"user_id": f"{self.user.id}"}
        )

        res_user_is_active = self.client.get(
            BORROWING_URL,
            {"user_id": f"{self.user.id}"}, {"is_active": "True"}
        )

        serializer1 = BorrowingSerializer(self.borrowing1)
        serializer2 = BorrowingSerializer(self.borrowing2)

        self.assertIn(serializer1.data, res_user.data)
        self.assertIn(serializer1.data, res_user_is_active.data)
        self.assertIn(serializer2.data, res_user_is_active.data)
