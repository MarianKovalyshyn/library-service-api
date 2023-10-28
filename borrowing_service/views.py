from math import ceil

from django.db import transaction
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
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
from payment_service.models import Payment
from payment_service.views import PaymentViewSet


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create_payment(self, borrowing: BorrowingSerializer) -> None:
        expected_return_date = borrowing.instance.expected_return_date
        borrow_date = borrowing.instance.borrow_date
        days = (expected_return_date - borrow_date).days
        money_to_pay = days * borrowing.instance.book.daily_fee
        result = ceil(money_to_pay) if money_to_pay >= 1 else 1

        payment = Payment.objects.create(
            borrowing=borrowing.instance,
            money_to_pay=result,
        )

        absolute_uri = self.request.build_absolute_uri(
            reverse("payment-service:payment-detail", kwargs={"pk": payment.id})
        )

        checkout_session = PaymentViewSet.create_checkout_session(
            result, absolute_uri
        )

        payment.session_url = checkout_session["session_url"]
        payment.session_id = checkout_session["session_id"]
        payment.save()


    def perform_create(self, serializer):
        with transaction.atomic():
            book_id = self.request.data.get("book")
            book = Book.objects.get(id=book_id)

            if book.inventory > 0:
                book.inventory -= 1
                book.save()
                serializer.save(user=self.request.user)
                self.create_payment(serializer)
            else:
                raise ValidationError({"error": "This book is not available"})

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user.is_staff and user_id:
            queryset = queryset.filter(user__id=int(user_id))
        elif not user.is_staff:
            queryset = queryset.filter(user=user)
        if is_active is not None:
            is_active = bool(is_active.lower() == "true")
            queryset = queryset.filter(
                Q(actual_return_date__isnull=True)
                if is_active
                else Q(actual_return_date__isnull=False)
            )

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id",
                type={"type": "number"},
                description="Filter by user id (ex. ?user_id=1).",
            ),
            OpenApiParameter(
                name="is_active",
                type=OpenApiTypes.BOOL,
                description="Filter by borrowing status"
                "Filter by active borrowings (ex. ?is_active=true). "
                "Filter by returned borrowings (ex. ?is_active=false)",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowingCreateSerializer

        if self.action == "list":
            return self.serializer_class

        if (
            self.action == "update" or self.action == "partial_update"
        ) and self.request.user.is_staff:
            return BorrowingSerializerWithUserData

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        if self.action == "return_borrowing":
            return BorrowingReturnSerializer

        if self.request.user.is_staff:
            return BorrowingSerializerWithUserData

        return self.serializer_class

    @action(detail=True, methods=["POST"])
    def return_borrowing(self, request, *args, **kwargs):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                {"error": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        book = borrowing.book
        book.inventory += 1
        book.save()

        borrowing.actual_return_date = timezone.now()

        if borrowing.actual_return_date > borrowing.expected_return_date:
            days_overdue = (
                borrowing.actual_return_date - borrowing.expected_return_date
            ).days
            fine_amount = ceil(days_overdue * borrowing.book.daily_fee * 2)
            checkout_session = PaymentViewSet.create_checkout_session(
                fine_amount, "http://library_service_api"
            )
            Payment.objects.create(
                borrowing=borrowing,
                money_to_pay=fine_amount,
                session_url=checkout_session["session_url"],
                session_id=checkout_session["session_id"],
                type="FINE",
            )

        borrowing.save()

        return Response(
            {"message": "Borrowing returned successfully"},
            status=status.HTTP_200_OK,
        )
