from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from book_service.serializers import BookSerializer

BOOK_LIST_URL = reverse("book_service:book-list")
BOOK_DETAIL_URL = reverse("book_service:book-detail", args=[1])


class UnauthenticatedBookApiTests(TestCase):
    def setUp(self):
        Book.objects.create(
            title="Test Book",
            author="Author Test",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )
        self.client = APIClient()

    def test_book_list_auth_not_required(self):
        res = self.client.get(BOOK_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_detail_auth_not_required(self):
        res = self.client.get(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_create_auth_required(self):
        res = self.client.post(BOOK_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_update_auth_required(self):
        res = self.client.put(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_partial_update_auth_required(self):
        res = self.client.patch(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_book_delete_auth_required(self):
        res = self.client.delete(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test_user",
            "pass123",
        )
        self.client.force_authenticate(self.user)

    def test_list_books(self):
        Book.objects.create(
            title="Test Book",
            author="Author Test",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )
        Book.objects.create(
            title="Test Book 2",
            author="Author Test 2",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )

        res = self.client.get(BOOK_LIST_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Author Test",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )

        res = self.client.get(BOOK_DETAIL_URL)

        serializer = BookSerializer(book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_book_create_is_staff_required(self):
        res = self.client.post(BOOK_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_update_is_staff_required(self):
        res = self.client.put(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_partial_update_is_staff_required(self):
        res = self.client.patch(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_delete_is_staff_required(self):
        res = self.client.delete(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "test_admin", "pass123"
        )
        self.client.force_authenticate(self.user)

    def test_book_create(self):
        payload = {
            "title": "Test Book",
            "author": "Author Test",
            "cover": "SOFT",
            "inventory": 2,
            "daily_fee": 5.55,
        }

        res = self.client.post(BOOK_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_book_update(self):
        Book.objects.create(
            title="Test Book",
            author="Author Test",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )
        payload = {
            "title": "Test Book 2",
            "author": "Author Test 2",
            "cover": "HARD",
            "inventory": 3,
            "daily_fee": 6.66,
        }

        res = self.client.put(BOOK_DETAIL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_partial_update(self):
        Book.objects.create(
            title="Test Book",
            author="Author Test",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )
        payload = {
            "title": "Test Book 2",
            "author": "Author Test 2",
        }

        res = self.client.patch(BOOK_DETAIL_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_book_delete(self):
        book = Book.objects.create(
            title="Test Book",
            author="Author Test",
            cover="SOFT",
            inventory=2,
            daily_fee=5.55,
        )

        res = self.client.delete(BOOK_DETAIL_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())
