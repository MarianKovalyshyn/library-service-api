from django.test import TestCase
from payment_service.models import Payment
from payment_service.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentSerializerTest(TestCase):
    def setUp(self):
        self.payment_data = {
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 3,
            "session_url": "https://test-url/",
            "session_id": "2",
            "money_to_pay": 300000.12,
        }
        self.payment = Payment.objects.create(**self.payment_data)

    def test_payment_list_serializer(self):
        serializer = PaymentListSerializer(instance=self.payment)
        expected_data = {
            "id": self.payment.id,
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 3,
            "session_url": "https://test-url/",
            "session_id": "2",
            "money_to_pay": "300000.12",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_payment_detail_serializer(self):
        serializer = PaymentDetailSerializer(instance=self.payment)
        expected_data = {
            "id": self.payment.id,
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 3,
            "session_url": "https://test-url/",
            "session_id": "2",
            "money_to_pay": "300000.12",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_create_invalid_data(self):
        invalid_data = {
            "status": "INVALID_STATUS",
            "type": "INVALID_TYPE",
            "borrowing_id": -1,
            "session_url": "invalid-url",
            "session_id": "",
            "money_to_pay": "invalid_amount",
        }
        serializer = PaymentListSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
