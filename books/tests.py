from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {"title": "Test Book", "author": "John Doe", "published_date": "2024-12-12"}

        # Create a book for testing
        self.book = Book.objects.create(
            title="Existing Book", author="Jane Doe", published_date="2024-12-12"
        )

    def test_get_books(self):
        """
        Test retrieving a list of books
        """
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Existing Book", str(response.data))

    def test_create_book(self):
        """
        Test creating a new book
        """
        response = self.client.post("/api/books/", data=self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Test Book", str(response.data))

    def test_create_book_validation_error(self):
        """
        Test creating a book with invalid data
        """
        invalid_data = {"title": "", "author": "John Doe"}
        response = self.client.post("/api/books/", data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Validation failed", str(response.data))
