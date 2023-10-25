from rest_framework import viewsets

from book_service.models import Book
# from book_service.serializers import BookSerializer
# from borrowing_service.permissions import IsAdminOrIfAuthenticatedReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
