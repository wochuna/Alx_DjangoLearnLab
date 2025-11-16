from django.urls import path
from .views import list_books, admin_view, librarian_view, member_view
from . views import LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from .import views
urlpatterns=[
    path('books/', list_books, name='book_list'),
    path('library/', LibraryDetailView.as_view(), name='library_detail'),
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
    path('add_book/', views.add_book_view, name='add_book'),
    path('edit_book/', views.change_book_view, name='edit_book'),
    path('delete_book/', views.delete_book_view, name='delete_book')

]
auth_patterns=[
    path('register/', views.register(template_name='relationship_app/register.htm'), name='register'),
    path('logout/', LogoutView.as_view(template_name='relationship/logout.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
]