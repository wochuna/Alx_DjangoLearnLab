from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'relationship_app'

urlpatterns = [
    # App Views
    path("", views.index, name="index"),
    path('books/', views.list_books, name='list_books'),  # URL for function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # URL for class-based view

    # Authentication
  path("login/", auth_views.LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
]  