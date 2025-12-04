from rest_framework import serializers
from .models import Author, Book
from django.utils import timezone

# Serializer for Book with custom validation on publication_year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate(self, data):
        if data['publication_year'] > timezone.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return data
    

# Serializer for Author with nested BookSerializer
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']