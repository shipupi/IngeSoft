from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
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

def register_page(request):
    context = {
        "title": "Register Page"
    }
    return render(request, "auth/view.html", context)

