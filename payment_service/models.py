from django.db import models

# from book_service.models import Borrowing


class Payment(models.Model):
    status = models.CharField(
        max_length=7,
        choices=[
            ("PENDING", "PENDING"),
            ("PAID", "PAID"),
        ]
    )
    type = models.CharField(
        max_length=7,
        choices=[
            ("PAYMENT", "PAYMENT"),
            ("FINE", "FINE"),
        ]
    )
    borrowing_id = models.IntegerField()
    session_url = models.URLField(max_length=255)
    session_id = models.CharField(max_length=63)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"Status: {self.status};"
            f" Type: {self.type};"
            f" Money to pay: {self.money_to_pay}"
        )
