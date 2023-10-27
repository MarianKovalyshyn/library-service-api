from django.db import models

from borrowing_service.models import Borrowing


class Payment(models.Model):
    """Model for payment, related to borrowing."""

    STATUS_CHOICES = (("PENDING", "PENDING"), ("PAID", "PAID"))
    TYPE_CHOICES = (("PAYMENT", "PAYMENT"), ("FINE", "FINE"))

    status = models.CharField(
        choices=STATUS_CHOICES, default="PENDING", max_length=50
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default="PAYMENT", max_length=50
    )
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.CharField(max_length=512)
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Money to pay {self.money_to_pay};"
