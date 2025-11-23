from django.shortcuts import render
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing book instances.
    
    Permissions:
    - All users must be authenticated to access the endpoints.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



