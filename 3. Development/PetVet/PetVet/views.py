from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm

def home_page(request):
    login_form = LoginForm(request.POST or None)
    context = {
            "title": "Home Page",
            "form" : login_form
    }
    if login_form.is_valid():
        print(login_form.cleaned_data)


    return render(request, "logreg/view.html", context)

def contact_page(request):
    context = {
        "title": "Contact Page"
    }
    return render(request, "logreg/view.html", context)

