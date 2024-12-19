from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author

class AuthorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_data = {"name": "Jane Doe", "biography": "Test biography"}
        
        # Create an author for testing
        self.author = Author.objects.create(name="John Doe", biography="Test biography")

    def test_get_authors(self):
        """
        Test retrieving a list of authors
        """
        response = self.client.get("/api/authors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("John Doe", str(response.data))

    def test_create_author(self):
        """
        Test creating a new author
        """
        response = self.client.post("/api/authors/", data=self.author_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("Jane Doe", str(response.data))

    def test_create_author_validation_error(self):
        """
        Test creating an author with invalid data
        """
        invalid_data = {"name": ""}
        response = self.client.post("/api/authors/", data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Validation failed", str(response.data))
