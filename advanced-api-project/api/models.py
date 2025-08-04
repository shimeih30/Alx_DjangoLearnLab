from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with validation for publication year.
    Includes all required fields and proper error handling.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        extra_kwargs = {
            'author': {'required': True}
        }

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                {"publication_year": "Publication year cannot be in the future"}
            )
        if value < 1800:  # Adding minimum year validation
            raise serializers.ValidationError(
                {"publication_year": "Publication year cannot be before 1800"}
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model with nested BookSerializer.
    Includes the related books through the 'books' related_name.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']