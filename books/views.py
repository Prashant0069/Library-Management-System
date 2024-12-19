from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer, BookDetailSerializer
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BookListCreateView(APIView):
    """
    List all books or create a new book
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve list of all books",
        responses={200: BookSerializer(many=True)},
    )
    def get(self, request):
        """
        Retrieve list of all books
        """
        try:
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while retrieving books: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Create a new book",
        request_body=BookSerializer,  
        responses={
            201: openapi.Response(
                description="Book created successfully",
                schema=BookSerializer,
            ),
            400: "Validation Error",
        },
    )
    def post(self, request):
        """
        Create a new book
        """
        serializer = BookSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Book created successfully!", "data": serializer.data},
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"error": "Validation failed", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError as e:
            return Response(
                {"error": f"Database error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BookDetailView(APIView):
    """
    Retrieve, update or delete a specific book
    """
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        """
        Helper method to get book instance
        """
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a specific books",
        responses={200: BookDetailSerializer(many=True)},
    )
    def get(self, request, pk):
        """
        Retrieve a specific book
        """
        book = self.get_object(pk)
        if not book:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = BookDetailSerializer(book)
        return Response(
            {"message": "Book retrieved successfully!", "data": serializer.data}
        )

    @swagger_auto_schema(
        operation_description="Update a specific book",
        request_body=BookDetailSerializer,
        responses={
            200: openapi.Response(
                description="Book updated successfully",
                schema=BookDetailSerializer
            ),
            400: openapi.Response(
                description="Validation Error",
            ),
            404: openapi.Response(
                description="Author not found",
            ),
        },
    )
    def put(self, request, pk):
        """
        Update a specific book
        """
        book = self.get_object(pk)
        if not book:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Book updated successfully!", "data": serializer.data}
            )
        return Response(
            {"error": "Validation failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a specific book",
        responses={200: BookDetailSerializer(many=True)},
    )
    def delete(self, request, pk):
        """
        Delete a specific book
        """
        book = self.get_object(pk)
        if not book:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        try:
            book.delete()
            return Response(
                {"message": "Book deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
