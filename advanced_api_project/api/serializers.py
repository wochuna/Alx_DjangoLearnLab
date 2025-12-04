from rest_framework import serializers
from  .models import Author, Book

# BookSerializer to serialize Book instances and validate publication year
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
# AuthorSerializer to serialize Author instances along with their related books using a nested serializer.
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name']
        fields = ['name', 'books']  
