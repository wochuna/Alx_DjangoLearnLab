from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm as RegisterForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .serializers import PostSerializer
from django.urls import reverse_lazy
from . models import Post, Comment, Tag
from . forms import PostForm, CommentForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



    # Handle user registration
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form}) 


# Handle user login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")      
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:    
            login(request, user)
            return redirect("profile")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "blog/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")



@login_required
def profile_view(request):
    return render(request, "blog/profile.html", {"user": request.user})


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
  
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template = 'blog/post_form.html'

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_confirm_delete.html'

def search_posts(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(content__icontains=query) 
            
        ).distinct()
    else:
        posts = Post.objects.all()
        
    serializer = PostSerializer(results, many=True)     
    return render(request, "blog/search_results.html", {"results": results, "query": query})


class PostByTagListView(ListView):

    model = Post
    template_name = "blog/posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        return Post.objects.filter(tags__slug=tag_slug).distinct()