from rest_framework import serializers
from .models import Author, Book
import datetime

# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation to ensure publication year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


# Serializer for the Author model, includes nested BookSerializer
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # Nested serialization of related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

"""
AuthorSerializer: Serializes Author instances and includes a nested list of books.
BookSerializer: Serializes Book instances with custom validation for publication_year.
"""
