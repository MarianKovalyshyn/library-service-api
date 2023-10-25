from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from customers_service.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            raise PermissionDenied("User not authenticated")
