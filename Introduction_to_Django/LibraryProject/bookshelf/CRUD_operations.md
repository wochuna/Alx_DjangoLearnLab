# Create a Book instance
from bookshelf.models import Book

Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

This creates a book with title 1984 by George Orwell published in 1949

# Retrieve all books
from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(f'Title: {book.title}, Author: {book.author}, Publication Year: {book.publication_year}')

This retrieves the book 1984 showing the title,author and year of publication

# Update Instance
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

This updates the book title from 1984 to Nineteen Eighty-Four

# Delete Instance
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete() # Delete

all_books = Book.objects.all()
print(all_books) # Confirm deletion

This deletes the book titled Nineteen Eighty-Four