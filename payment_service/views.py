from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from payment_service.models import Payment
from payment_service.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "update":
            return PaymentDetailSerializer
        return PaymentListSerializer

    def get_permissions(self):
        if self.action in ["list", "create"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
