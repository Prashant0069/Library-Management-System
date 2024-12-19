from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BorrowRecordCreateView(APIView):
    """
    Create a new borrow record
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new borrow record",
        request_body=BorrowRecordSerializer,  
        responses={
            201: openapi.Response(
                description="Borrow record created successfully",
                schema=BorrowRecordSerializer,
            ),
            400: "Validation Error",
        },
    )
    def post(self, request):
        """
        Create a new borrow record
        Automatically reduces available book copies
        """
        serializer = BorrowRecordSerializer(data=request.data)
        try:
            if serializer.is_valid():
                borrow_record = serializer.save()
                # Check if the book is available
                if not borrow_record.book.is_available():
                    borrow_record.delete()
                    return Response(
                        {"error": "Book is not available for borrowing"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Reduce available copies
                borrow_record.book.reduce_copies()
                return Response(
                    {"message": "Borrow record created successfully!", "data": serializer.data},
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

class BorrowRecordReturnView(APIView):
    """
    Return a borrowed book
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get borrow record instance
        """
        try:
            return BorrowRecord.objects.get(pk=pk)
        except BorrowRecord.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Mark a borrowed book as returned",
        request_body=BorrowRecordSerializer,
        responses={
            200: openapi.Response(
                description="Borrowed book returned successfully",
                schema=BorrowRecordSerializer
            ),
            400: openapi.Response(
                description="Validation Error",
            ),
            404: openapi.Response(
                description="Borrowed book not found",
            ),
        },
    )
    def put(self, request, pk):
        """
        Mark a borrowed book as returned
        Increases available book copies
        """
        borrow_record = self.get_object(pk)

        if not borrow_record:
            return Response(
                {"error": "Borrow record not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if already returned
        if borrow_record.return_date:
            return Response(
                {"error": "This book has already been returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Mark book as returned
            borrow_record.mark_as_returned()
            borrow_record.book.increase_copies()
            
            serializer = BorrowRecordSerializer(borrow_record)
            return Response(
                {"message": "Book returned successfully!", "data": serializer.data}
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
