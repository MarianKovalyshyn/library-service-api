from django.test import TestCase

from book_service.models import Book
from book_service.serializers import BookSerializer


class BookSerializerTest(TestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Author Test",
            "cover": "COVER",
            "inventory": 2,
            "daily_fee": 5.55,
        }
        self.book = Book.objects.create(**self.book_data)

    def test_serializer_output(self):
        serializer = BookSerializer(instance=self.book)
        expected_data = {
            "title": "Test Book",
            "author": "Author Test",
            "cover": "COVER",
            "inventory": 2,
            "daily_fee": 5.55,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_valid_serializer(self):
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        payload = {
            "title": "Invalid Book",
            "cover": "Author Test",
            "inventory": 2,
            "daily_fee": 5.55,
        }
        serializer = BookSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
