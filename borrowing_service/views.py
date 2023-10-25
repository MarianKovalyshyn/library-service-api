from rest_framework import viewsets

from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing
    serializer_class = BorrowingSerializer
