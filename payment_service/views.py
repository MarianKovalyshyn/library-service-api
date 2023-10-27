import stripe

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from payment_service.models import Payment
from payment_service.serializers import PaymentSerializer, PaymentListSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related(
        "borrowing",
        "borrowing__book",
        "borrowing__user"
    )
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return PaymentListSerializer
        return self.serializer_class

    def get_queryset(self):
        is_staff = self.request.query_params.get("is_staff")
        if not is_staff:
            return self.queryset.filter(borrowing__user=self.request.user)
        return self.queryset

    @staticmethod
    def create_checkout_session(money_to_pay: int, domain: str):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain + "success/",
                cancel_url=domain + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": money_to_pay,
                        "product_data": {
                            "name": "Borrowed book",
                        },
                    },
                    "quantity": 1,
                }],
            )
            return {"session_id": checkout_session["id"], "session_url": checkout_session["url"]}
        except Exception as e:
            return {"error": str(e)}

    @action(detail=True, methods=["GET"], url_path="success")
    def success(self, request, *args, **kwargs):
        payment = self.get_object()
        session_id = payment.session_id

        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == "paid":
            payment.status = "PAID"
            payment.save()
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Payment is cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=["GET"], url_path='cancelled')
    def cancel(self, request, *args, **kwargs):
        return Response(
            {"message": "Your payment wasn't successful. Please, try again."},
            status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@require_POST
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        if event["type"] == "payment_intent.succeeded":
            Payment.objects.filter(payment_id=event["data"]["object"]["id"]).update(status="PAID")

        if event["type"] == "payment_intent.payment_failed":
            Payment.objects.filter(payment_id=event["data"]["object"]["id"]).update(status="FAILED")

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    return HttpResponse(status=400)
