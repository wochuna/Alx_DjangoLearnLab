from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test,login_required
from .models import UserProfile


from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def _has_role(user, role):
    return user.is_authenticated and user.userprofile.role == role

@user_passes_test(lambda u: _has_role(u, 'Admin'), login_url='login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)


# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
def index(request):
    return render(request, 'relationship_app/index.html')   

# Registrarion View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def _has_role(user, role):
    if not user.is_authenticated:
        return False
    # use related_name 'userprofile' added above
    profile = getattr(user, 'userprofile', None)
    return bool(profile and profile.role == role)

# Admin-only view
@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_ADMIN), login_url='relationship_app:login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian-only view
@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_LIBRARIAN), login_url='relationship_app:login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member-only view
@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_MEMBER), login_url='relationship_app:login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')
