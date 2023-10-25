from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateTimeField()
    expected_return_date = models.DateTimeField()
    actual_return_date = models.DateTimeField()
    book_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        ordering = ["-borrow_date"]

    def __str__(self):
        return (
            f"User_id: {self.user_id}\n" 
            f"Book id: {self.book_id}\n"
            f"Borrow date: {self.borrow_date},\n"
            f"Expected return date: {self.expected_return_date}\n"
            f"Actual return date: {self.actual_return_date}"
        )
