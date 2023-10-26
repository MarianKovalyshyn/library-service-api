from django.urls import path, include
from rest_framework import routers

from borrowing_service.views import BorrowingViewSet, ReturnBorrowingView

router = routers.DefaultRouter()

router.register("borrowings", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "return/<int:borrowing_id>/",
        ReturnBorrowingView.as_view(),
        name="return-borrowing",
    ),
]

app_name = "borrowing-service"
