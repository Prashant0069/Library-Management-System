from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model to handle CRUD operations
    """
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio']
        read_only_fields = ['id']

class AuthorDetailSerializer(AuthorSerializer):
    """
    Detailed serializer that includes book information
    """
    books = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(AuthorSerializer.Meta):
        fields = ['id', 'name', 'bio', 'books']