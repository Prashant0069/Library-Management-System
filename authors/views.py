from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Author
from .serializers import AuthorSerializer, AuthorDetailSerializer
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AuthorListCreateView(APIView):
    """
    List all authors or create a new author
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve list of all authors",
        responses={200: AuthorSerializer(many=True)},
    )
    def get(self, request):
        """
        Retrieve list of all authors
        """
        try:
            authors = Author.objects.all()
            serializer = AuthorSerializer(authors, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while retrieving authors: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Create a new author",
        request_body=AuthorSerializer,  
        responses={
            201: openapi.Response(
                description="Author created successfully",
                schema=AuthorSerializer,
            ),
            400: "Validation Error",
        },
    )
    def post(self, request):
        """
        Create a new author
        """
        serializer = AuthorSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Author created successfully!", "data": serializer.data},
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

class AuthorDetailView(APIView):
    """
    Retrieve, update or delete a specific author
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        """
        Helper method to get author instance
        """
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve s specific author",
        responses={200: AuthorDetailSerializer(many=True)},
    )
    def get(self, request, pk):
        """
        Retrieve a specific author
        """
        author = self.get_object(pk)
        if not author:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = AuthorDetailSerializer(author)
        return Response(
            {"message": "Author retrieved successfully!", "data": serializer.data}
        )

    @swagger_auto_schema(
        operation_description="Update a specific author",
        request_body=AuthorDetailSerializer,
        responses={
            200: openapi.Response(
                description="Author updated successfully",
                schema=AuthorDetailSerializer
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
        Update a specific author
        """
        author = self.get_object(pk)
        if not author:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Author updated successfully!", "data": serializer.data}
            )
        return Response(
            {"error": "Validation failed", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        operation_description="Delete a specific author",
        responses={200: AuthorDetailSerializer(many=True)},
    )
    def delete(self, request, pk):
        """
        Delete a specific author
        """
        author = self.get_object(pk)
        if not author:
            return Response(
                {"error": "Author not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        try:
            author.delete()
            return Response(
                {"message": "Author deleted successfully!"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
