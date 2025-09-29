from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # Django session login
            # ✅ Also issue JWT
            refresh = RefreshToken.for_user(user)
            response = redirect("home")
            response.set_cookie("access_token", str(refresh.access_token), httponly=True)
            response.set_cookie("refresh_token", str(refresh), httponly=True)
            messages.success(request, "Logged in successfully")
            return response
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "users/login.html")

# ✅ Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("users:login")  # back to login page with modal

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("/")

    return redirect("users:login")  # only allow POST
