from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import timedelta, datetime
from django.utils import timezone

from book_service.models import Book
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
)


def create_user(**params):
    return get_user_model().objects.create_user(**params)


def datetime_to_iso(time):
    date_string = str(time)
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f%z")
    serializer_date_format = (
        dt.astimezone(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )
    return serializer_date_format


class BorrowingSerializerTest(TestCase):
    def setUp(self):
        self.borrowing_data = {
            "expected_return_date": timezone.now() + timedelta(days=1),
            "book": Book.objects.create(
                title="test_title",
                author="test_author",
                daily_fee=20.50,
                cover="SOFT",
                inventory=5,
            ),
            "user": get_user_model().objects.create_user(
                "test@test.com",
                "password123",
            ),
        }

        self.borrowing = Borrowing.objects.create(**self.borrowing_data)

    def test_serializer_output(self):
        serializer = BorrowingSerializer(instance=self.borrowing)

        expected_data = {
            "id": self.borrowing.id,
            "borrow_date": datetime_to_iso(self.borrowing.borrow_date),
            "expected_return_date": datetime_to_iso(
                self.borrowing.expected_return_date
            ),
            "actual_return_date": self.borrowing.actual_return_date,
            "book": self.borrowing.book.title,
            "user": self.borrowing.user.email,
            "payments": [],
        }

        self.assertEqual(serializer.data, expected_data)

    def test_valid_create_serializer(self):
        payload = {
            "expected_return_date": timezone.now() + timedelta(days=1),
            "book": self.borrowing.book.id,
        }

        serializer = BorrowingCreateSerializer(data=payload)

        self.assertTrue(serializer.is_valid())

    def test_invalid_create_serializer(self):
        payload = {
            "expected_return_date": timezone.now() - timedelta(days=1),
            "book": self.borrowing.book.id,
        }

        serializer = BorrowingCreateSerializer(data=payload)

        self.assertFalse(serializer.is_valid())
