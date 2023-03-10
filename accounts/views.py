from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def logout_user(request):
    logout(request)
    return redirect("login-page")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("databank-page")
        else:
            messages.info(request, "Username OR password is incorrect")
    
    return render(request, "accounts/login.html")
