from datetime import date

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


class ReturnBorrowingView(APIView):
    @staticmethod
    def post(request, borrowing_id):
        borrowing = Borrowing.objects.get(id=borrowing_id)

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Borrowing has already been returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        borrowing.actual_return_date = date.today()
        borrowing.is_active = False
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response(
            {"detail": "Borrowing returned successfully"}, status=status.HTTP_200_OK
        )
