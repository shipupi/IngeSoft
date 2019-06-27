from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm

def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
            "title": "Login Page",
            "form" : login_form
    }
    print("User logged in?")
    print(request.user.is_authenticated)
    if login_form.is_valid():
        print(login_form.cleaned_data)
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #success page
            login(request, user)
            #context['form'] = LoginForm()
            return redirect('/home')
        else:
            #failure page
            print("Error")

    return render(request, "auth/view.html", context)

User = get_user_model()
def register_page(request):
    register_form = RegisterForm(request.POST or None)
    context = {
        "title": "Register Page",
        "form" : register_form
    }
    if register_form.is_valid():
        print(register_form.cleaned_data)
        username = register_form.cleaned_data.get("username")
        email = register_form.cleaned_data.get("email")
        password = register_form.cleaned_data.get("password")
        new_user = User.objects.create_user(username=username, email=email,
                password=password)
        print(new_user)
    return render(request, "auth/view.html", context)

def cart_page(request):
    context = {
        "title": "Shopping Cart"
    }
    return render(request, "auth/view.html", context)


