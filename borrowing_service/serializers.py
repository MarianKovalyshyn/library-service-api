from rest_framework import serializers

import book_service.serializers
import customers_service.serializers
from borrowing_service.models import Borrowing


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "expected_return_date")


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField("title", read_only=True)
    user = serializers.StringRelatedField()

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

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "actual_return_date",
            "expected_return_date",
            "book",
            "user",
        )


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book")
