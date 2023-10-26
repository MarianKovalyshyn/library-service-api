from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from book_service.models import Book
from borrowing_service.models import Borrowing


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestBorrowingModel(TestCase):
    def test_borrowing_str_method(self):
        expected_return_date = timezone.now() + timezone.timedelta(days=14)
        book = Book.objects.create(
            title="test_title",
            author="test_author",
            daily_fee=20.50,
            cover="SOFT",
            inventory=5,
        )
        payload = {
            "email": "test@test.com",
            "password": "testpass",
        }
        user = create_user(**payload)

        borrowing = Borrowing.objects.create(
            expected_return_date=expected_return_date,
            book=book,
            user=user,
        )

        expected_str = (
            f"User: {user.email}\n"
            f"Book: {book.title}\n"
            f"Borrow date: {borrowing.borrow_date},\n"
            f"Expected return date: {expected_return_date}\n"
            f"Actual return date: {borrowing.actual_return_date}"
        )

        self.assertEqual(str(borrowing), expected_str)
