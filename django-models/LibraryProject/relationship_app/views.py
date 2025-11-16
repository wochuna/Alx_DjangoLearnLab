from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse

from .models import Book, Library

def user_role(role):
    def check(user):
        return hasattr(user, "userprofile") and getattr(user.userprofile, "role", None) == role
    return check

# Admin-only view
@user_passes_test(user_role("Admin"), login_url="relationship_app:login")
def admin_view(request):
    return render(request, "relationship_app/admin_view.html", {"role": "Admin"})

# Librarian-only view
@user_passes_test(user_role("Librarian"), login_url="relationship_app:login")
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html", {"role": "Librarian"})

# Member-only view
@user_passes_test(user_role("Member"), login_url="relationship_app:login")
def member_view(request):
    return render(request, "relationship_app/member_view.html", {"role": "Member"})


def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


def index(request):
    return render(request, "relationship_app/index.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("relationship_app:list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Permission-protected placeholders (return simple responses to avoid syntax errors)
@permission_required("relationship_app.add_book", raise_exception=True)
def add_book_view(request):
    return HttpResponse("Add book view (protected)")

@permission_required("relationship_app.change_book", raise_exception=True)
def change_book_view(request):
    return HttpResponse("Change book view (protected)")

@permission_required("relationship_app.delete_book", raise_exception=True)
def delete_book_view(request):
    return HttpResponse("Delete book view (protected)")