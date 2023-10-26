from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from book_service.models import Book
from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingSerializerWithUserData,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            book_id = self.request.data.get("book")
            book = Book.objects.get(id=book_id)

            if book.inventory > 0:
                book.inventory -= 1
                book.save()
                serializer.save()
            else:
                return Response(
                    {"error": "This book is not available"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def get_queryset(self):
        queryset = self.queryset
        is_staff = self.request.query_params.get("is_staff")
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if not is_staff:
            queryset = queryset.filter(user_id=self.request.user.id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if is_active:
            queryset = queryset.filter(
                expected_return_date__gte=timezone.now()
            )

        return queryset

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return BorrowingSerializerWithUserData

        if self.action == "retrieve":
            BorrowingDetailSerializer

        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        if self.action == "create":
            return BorrowingCreateSerializer

        return self.serializer_class

    @action(detail=True, methods=["POST"])
    def return_borrowing(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"error": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book_id = self.request.data.get("book")
        book = Book.objects.get(id=book_id)

        book.inventory += 1
        book.save()

        borrowing.actual_return_date = timezone.now()
        borrowing.save()

        return Response(
            {"message": "Borrowing returned successfully"},
            status=status.HTTP_200_OK,
        )
