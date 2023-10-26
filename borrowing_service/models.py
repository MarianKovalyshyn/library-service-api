from django.conf import settings
from django.db import models
from django.db.models import Q, F

from book_service.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateTimeField(auto_now_add=True)
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-borrow_date"]
        constraints = [
            models.CheckConstraint(
                check=Q(expected_return_date__gte=F("borrow_date"))
                | Q(actual_return_date__gte=F("borrow_date")),
                name="valid_return_date",
            )
        ]

    def __str__(self):
        return (
            f"User: {self.user.email}\n"
            f"Book: {self.book.title}\n"
            f"Borrow date: {self.borrow_date},\n"
            f"Expected return date: {self.expected_return_date}\n"
            f"Actual return date: {self.actual_return_date}"
        )
