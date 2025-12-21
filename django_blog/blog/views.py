from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm as RegisterForm
from django.contrib import messages



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