from rest_framework import serializers
from .models import Book
from authors.models import Author

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model to handle CRUD operations
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'available_copies']
        read_only_fields = ['id']

    def validate_author(self, value):
        """
        Ensure the author exists
        """
        try:
            Author.objects.get(id=value.id)
        except Author.DoesNotExist:
            raise serializers.ValidationError("Invalid author")
        return value

class BookDetailSerializer(BookSerializer):
    """
    Detailed serializer that includes additional book information
    """
    author_name = serializers.SerializerMethodField()

    class Meta(BookSerializer.Meta):
        fields = ['id', 'title', 'author', 'author_name', 'isbn', 'available_copies']

    def get_author_name(self, obj):
        return obj.author.name