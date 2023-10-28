from rest_framework import serializers

from payment_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ("status", "type", "session_url", "session_id", "money_to_pay",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["borrowing"] = f"{instance.borrowing.book.title} - {instance.borrowing.user.email}"
        return data


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "status", "type", "money_to_pay",)
