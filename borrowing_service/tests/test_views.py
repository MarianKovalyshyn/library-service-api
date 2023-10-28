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
    BorrowingSerializer,
    BorrowingDetailSerializer,
)


BORROWING_URL = reverse("borrowing-service:borrowing-list")


def sample_user(**params):
    defaults = {
        "email": "test@test.com",
        "password": "password",
    }

    defaults.update(params)

    return get_user_model().objects.create_user(**defaults)


def sample_superuser(**params):
    defaults = {
        "email": "admin@test.com",
        "password": "password",
    }

    defaults.update(params)

    return get_user_model().objects.create_superuser(**defaults)


def sample_book(**params):
    defaults = {
        "title": "book",
        "author": "author",
        "inventory": 10,
        "daily_fee": 0.25,
    }

    defaults.update(params)

    return Book.objects.create(**defaults)


def sample_borrowing(**params):
    defaults = {
        "user": sample_user(),
        "book": sample_book(),
        "expected_return_date": timezone.now() + timedelta(days=1),
    }

    defaults.update(params)

    return Borrowing.objects.create(**defaults)


def detail_url(borrowing_id: int):
    return reverse("borrowing-service:borrowing-detail", args=[borrowing_id])


class TestUnauthenticatedBorrowing(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAuthenticatedBorrowing(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.borrowing = sample_borrowing()
        self.client.force_authenticate(self.borrowing.user)
        self.serializer = BookSerializer(self.borrowing.book)

    def test_list_borrowings(self):
        response = self.client.get(BORROWING_URL)

        borrowings = Borrowing.objects.filter(user=self.borrowing.user)
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

        self.borrowing1 = sample_borrowing(user=sample_superuser())
        self.borrowing2 = Borrowing.objects.create(
            book=sample_book(title="book2"),
            user=self.borrowing1.user,
            actual_return_date=timezone.now() + timedelta(hours=5),
            expected_return_date=timezone.now() + timedelta(days=1),
        )

        self.client.force_authenticate(self.borrowing1.user)

        self.serializer1 = BookSerializer(self.borrowing1.book)
        self.serializer2 = BookSerializer(self.borrowing2.book)

    def test_borrowings_filter(self):
        response_user = self.client.get(
            BORROWING_URL, {"user_id": f"{self.borrowing1.user.id}"}
        )

        response_user_is_active = self.client.get(
            BORROWING_URL,
            {"user_id": f"{self.borrowing1.user.id}"},
            {"is_active": "True"},
        )

        serializer1 = BorrowingSerializer(self.borrowing1)
        serializer2 = BorrowingSerializer(self.borrowing2)

        self.assertIn(serializer1.data, response_user.data)
        self.assertIn(serializer1.data, response_user_is_active.data)
        self.assertIn(serializer2.data, response_user_is_active.data)


class TestAdminBorrowingViewSet(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = sample_superuser()
        self.client.force_authenticate(self.admin_user)

    def test_filter_user_borrowings_by_id(self):
        self.borrowing = sample_borrowing()
        url = BORROWING_URL + f"?user_id={self.borrowing.user.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestReturnBook(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.borrowing = sample_borrowing()
        self.client.force_authenticate(self.borrowing.user)

    def test_return_book(self):
        response = self.client.post(
            f"http://127.0.0.1:8000/api/borrowing-service/borrowings/"
            f"{self.borrowing.id}/return_borrowing/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"message": "Borrowing returned successfully"}
        )
        self.borrowing.refresh_from_db()
        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.borrowing.book.refresh_from_db()
        self.assertEqual(self.borrowing.book.inventory, 11)
