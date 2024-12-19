from rest_framework import serializers
from .models import BorrowRecord
from books.models import Book

class BorrowRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for BorrowRecord model to handle borrowing and returning books
    """
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'borrowed_by', 'borrow_date', 'return_date']
        read_only_fields = ['id', 'borrow_date', 'return_date']

    def validate_book(self, value):
        """
        Check if book is available for borrowing
        """
        if value.available_copies <= 0:
            raise serializers.ValidationError("No copies of this book are currently available")
        return value

    def create(self, validated_data):
        """
        Custom create method to reduce available copies
        """
        book = validated_data['book']
        book.reduce_available_copies()
        return BorrowRecord.objects.create(**validated_data)