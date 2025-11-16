from django.urls import path
from . import views
from .views import list_books,admin_view,librarian_view,member_view
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView as LogoutView


urlpatterns = [
    # App Views
    path('books/', views.list_books, name='list_books'),  # URL for function-based view
    path('library/', LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
  

    # Authentication
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register(template_name='relationship_app/register.html'), name="register"),
]  