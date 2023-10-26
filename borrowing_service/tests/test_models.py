from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from book_service.models import Book
from borrowing_service.models import Borrowing


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestBorrowingModel(TestCase):
    def test_borrowing_str_method(self):
        payload = {
            "email": "tes1t@test.com",
            "password": "testpass",
        }
        borrow_date = timezone.now()
        expected_return_date = borrow_date + timezone.timedelta(days=14)
        actual_return_date = borrow_date + timezone.timedelta(days=10)
        book = Book.objects.create(
            title="test_title",
            author="test_author",
            daily_fee=20.50,
            cover="SOFT",
            inventory=5
        )
        user = create_user(**payload)

        borrowing = Borrowing.objects.create(
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
            actual_return_date=actual_return_date,
            book=book,
            user=user,
        )

        expected_str = (
            f"User: {user.email}\n"
            f"Book: {book.title}\n"
            f"Borrow date: {borrow_date},\n"
            f"Expected return date: {expected_return_date}\n"
            f"Actual return date: {actual_return_date}"
        )

        self.assertEqual(str(borrowing), expected_str)
