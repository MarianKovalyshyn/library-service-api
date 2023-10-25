from django.test import TestCase
from django.utils import timezone

from borrowing_service.models import Borrowing


class TestBorrowingModel(TestCase):
    def test_borrowing_str_method(self):
        borrow_date = timezone.now()
        expected_return_date = borrow_date + timezone.timedelta(days=14)
        actual_return_date = borrow_date + timezone.timedelta(days=10)
        book_id = 1
        user_id = 1

        borrowing = Borrowing.objects.create(
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
            actual_return_date=actual_return_date,
            book_id=book_id,
            user_id=user_id,
        )

        expected_str = (
            f"User_id: {user_id}\n"
            f"Book id: {book_id}\n"
            f"Borrow date: {borrow_date},\n"
            f"Expected return date: {expected_return_date}\n"
            f"Actual return date: {actual_return_date}"
        )

        self.assertEqual(str(borrowing), expected_str)
