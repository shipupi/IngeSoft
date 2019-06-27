from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                        "id": "log_full_name",
                        "placeholder": "Your full name"
                })
            )
    password = forms.CharField(
        widget=forms.PasswordInput(
                attrs={
                    "class": "form-control",
                        "id": "log_pass_name",
                        "placeholder": "Your password"
                })

    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
                attrs={
                    "class": "form-control",
                        "id": "log_pass2",
                        "placeholder": "Please renter your password"
                })

    )

    email = forms.EmailField(
        widget=forms.EmailInput(
                attrs={
                    "class": "form-control",
                        "id": "log_user_name",
                        "placeholder": "Your email"
                })

    )

    def clean(self):
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")
        username = data.get("username")
        qs= User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username already taken")

        if password2 != password:
            raise forms.ValidationError("Passwords don't match")

        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail")

        #validacion de mismo mail
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already taken")

        return data
