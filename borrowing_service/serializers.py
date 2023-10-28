from django.utils import timezone
from rest_framework import serializers

import book_service.serializers
import customers_service.serializers
import payment_service.serializers
from borrowing_service.models import Borrowing


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "expected_return_date")

    def validate_expected_return_date(self, expected_return_date):
        if expected_return_date <= timezone.now():
            raise serializers.ValidationError(
                "Expected return date cannot be less than the current date."
            )
        return expected_return_date


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField("title", read_only=True)
    user = serializers.StringRelatedField()
    payments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )


class BorrowingSerializerWithUserData(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        book = instance.book
        representation["book"] = f"{book.title} - {book.author}"
        return representation


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = book_service.serializers.BookSerializer()
    user = customers_service.serializers.UserSerializer()
    payments = payment_service.serializers.PaymentSerializer(many=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "actual_return_date",
            "expected_return_date",
            "book",
            "user",
            "payments",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id",)
