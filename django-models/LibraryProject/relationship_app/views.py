from django.shortcuts import render,redirect
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
def index(request):
    return render(request, 'relationship_app/index.html')       
