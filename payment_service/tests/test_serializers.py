from django.test import TestCase

from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer


class PaymentSerializerTest(TestCase):
    def setUp(self):
        self.payment_data = {
            "id": 1,
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 3,
            "session_url": "https://test-url/",
            "session_id": "2",
            "money_to_pay": 300000.12,
        }
        self.payment = Payment.objects.create(**self.payment_data)

    def test_serializer_output(self):
        serializer = PaymentSerializer(instance=self.payment)
        expected_data = {
            "id": 1,
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 3,
            "session_url": "https://test-url/",
            "session_id": "2",
            "money_to_pay": "300000.12",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_invalid_serializer(self):
        payload = {
            "id": 1,
            "status": "PENDING",
            "type": "FINE",
            "borrowing_id": 3,
            "session_url": "https://test-url/",
            "session_id": "2",
            "money_to_pay": 300000.12,
        }
        serializer = PaymentSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
