# Delete Instance
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete() # Delete

all_books = Book.objects.all()
print(all_books) # Confirm deletion
