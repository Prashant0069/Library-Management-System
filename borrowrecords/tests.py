from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import BorrowRecord, Book, User

class BorrowRecordAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author="Author Name",
            total_copies=5,
            available_copies=5
        )

        # Create a borrow record
        self.borrow_record = BorrowRecord.objects.create(
            user=self.user,
            book=self.book
        )

    def test_create_borrow_record(self):
        """
        Test creating a new borrow record
        """
        data = {"book": self.book.id}
        response = self.client.post("/api/borrow-records/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Borrow record created successfully!", str(response.data))

    def test_return_borrow_record(self):
        """
        Test returning a borrowed book
        """
        response = self.client.put(f"/api/borrow-records/{self.borrow_record.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Book returned successfully!", str(response.data))

    def test_return_already_returned_book(self):
        """
        Test returning a book that has already been returned
        """
        self.borrow_record.mark_as_returned()  # Manually mark as returned
        response = self.client.put(f"/api/borrow-records/{self.borrow_record.id}/return/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This book has already been returned", str(response.data))
