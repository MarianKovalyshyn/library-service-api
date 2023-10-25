from django.test import TestCase

from book_service.models import Book


class BookTests(TestCase):
    def test_car_str(self):
        book = Book.objects.create(
            title="test_title",
            author="test_author",
            daily_fee=20.50,
            cover="SOFT",
            inventory=5
        )
        self.assertEqual(
            str(book),
            f"Title:{book.title};"
            f" Author: {book.author};"
            f" Daily fee: {book.daily_fee}"
        )
