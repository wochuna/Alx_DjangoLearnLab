import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

import django
django.setup()

from relationship_app.models import Author, Book, Library, Librarian
from django.core.exceptions import ObjectDoesNotExist

def books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
    except ObjectDoesNotExist:
        print(f"No author found with name: {author_name}")
        return
    books_via_filter = Book.objects.filter(author=author)
    print(f"\nBooks by {author.name} (via Book.objects.filter):")
    for b in books_via_filter:
        print(f"- {b.title}")

    
    
def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except ObjectDoesNotExist:
        print(f"No library found with name: {library_name}")
        return
    books = library.books.all()  # ManyToManyField
    print(f"Books in library '{library.name}':")
    for b in books:
        print(f"- {b.title} by {b.author.name}")

def librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
    except ObjectDoesNotExist:
        print(f"No library found with name: {library_name}")
        return
    # OneToOne
    try:
        librarian = library.librarian
    except ObjectDoesNotExist:
        print(f"No librarian assigned to library '{library.name}'")
        return
    print(f"Librarian for '{library.name}': {librarian.name}")

if __name__ == "__main__":
    # Example usages
    books_by_author("Paulin Kea")
    print()
    books_in_library("Katiba")
    print()
    librarian_for_library("Asha")
