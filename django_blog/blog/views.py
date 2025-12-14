from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import  authenticate, login, logout
from django.urls import reverse, NoReverseMatch
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # respect 'next' parameter if provided
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url:
                return redirect(next_url)
            # try named URL 'index', otherwise fallback to root
            try:
                return redirect(reverse("index"))
            except Exception:
                return redirect("/")
        messages.error(request, "Invalid username or password.")
        return render(request, "registration/login.html", {"username": username})
    return render(request, "registration/login.html")


def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    return render(request, 'registration/profile.html')

def index(request):
    return redirect('profile')