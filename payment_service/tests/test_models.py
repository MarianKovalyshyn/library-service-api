from django.test import TestCase

from payment_service.models import Payment


class PaymentTests(TestCase):
    def test_payment_str(self):
        payment = Payment.objects.create(
            status="PENDING",
            type="FINE",
            borrowing_id=3,
            session_url="https://test-url/",
            session_id=2,
            money_to_pay=300000.12,
        )
        self.assertEqual(
            str(payment),
            f"Status: {payment.status};"
            f" Type: {payment.type};"
            f" Money to pay: {payment.money_to_pay}"
        )
