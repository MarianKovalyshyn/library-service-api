from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from payment_service.models import Payment
from payment_service.serializers import (
    PaymentDetailSerializer,
    PaymentListSerializer,
)


class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentDetailSerializer
    permission_classes = [IsAuthenticated]
