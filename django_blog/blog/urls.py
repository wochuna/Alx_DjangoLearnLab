from django.urls import path
from .views import register_view, login_view, logout_view, profile_view, \
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    CommentCreateView, CommentUpdateView, CommentDeleteView, PostByTagListView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts_by_tag"),
]

post_urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", .as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
] +  urlpatterns


comment_urlpatterns = [
    path("comments/", CommentCreateView.as_view, name="comment_list"),
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
] + post_urlpatterns + urlpatterns


