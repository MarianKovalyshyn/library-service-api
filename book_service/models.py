from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=63)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=7,
        choices=[("SOFT", "SOFT"), ("HARD", "HARD")]
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return (f"Title:{self.title};"
                f" Author: {self.author};"
                f" Daily fee: {self.daily_fee}")
