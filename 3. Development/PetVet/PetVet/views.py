from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm

#---------------------- LOGIN ------------------------#
def login_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
            "title": "Login Page",
            "form" : login_form
    }
    #print("User logged in?")
    #print(request.user.is_authenticated)
    if login_form.is_valid():
        print(login_form.cleaned_data)
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #success page
            login(request, user)
            context['form'] = LoginForm()
            return redirect('/')
        else:
            #failure page
            print("Error: Incorrect login")

    return render(request, "auth/login.html", context)

#-------------------- REGISTRATION ---------------------#
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
        
        # Redirect the user to the registration complete page
        return redirect(reverse('register_complete_page'))

    return render(request, "auth/register.html", context)

#------------- REGISTRATION COMPLETE ----------------#
def register_complete_page(request):
    template = 'auth/register_complete.html'
    return render(request, template, {})

def index(request):
    template = 'index/index.html'
    return render(request, template, {})

#---------------------- CART ------------------------#
def cart_page(request):
    context = {
        "title": "Shopping Cart"
    }
    return render(request, "auth/view.html", context)


