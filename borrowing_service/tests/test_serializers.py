from django.test import TestCase

from datetime import datetime

from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer


class BorrowingSerializerTest(TestCase):
    def setUp(self):
        self.borrowing_data = {
            "borrow_date": datetime(2023, 9, 25, 14, 0),
            "expected_return_date": datetime(2024, 1, 25, 10, 0),
            "actual_return_date": datetime(2023, 10, 25, 14, 0),
            "book_id": 1,
            "user_id": 2,
        }
        self.borrowing = Borrowing.objects.create(**self.borrowing_data)

    def test_serializer_output(self):
        serializer = BorrowingSerializer(instance=self.borrowing)
        expected_data = {
            "id": self.borrowing.id,
            "borrow_date": "2023-09-25T14:00:00Z",
            "expected_return_date": "2024-01-25T10:00:00Z",
            "actual_return_date": "2023-10-25T14:00:00Z",
            "book_id": self.borrowing.book_id,
            "user_id": self.borrowing.user_id,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_valid_serializer(self):
        serializer = BorrowingSerializer(data=self.borrowing_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        payload = {
            "borrow_date": datetime(2023, 9, 25, 14, 0),
            "expected_return_date": datetime(2024, 1, 25, 10, 0),
            "actual_return_date": datetime(2023, 10, 25, 14, 0),
            "book_id": "book title",
        }
        serializer = BorrowingSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
