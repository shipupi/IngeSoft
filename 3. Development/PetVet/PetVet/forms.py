from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    fullname = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                        "id": "log_full_name",
                        "placeholder": "Your full name"
                })
            )
    password = forms.CharField(
        widget=forms.TextInput(
                attrs={
                    "class": "form-control",
                        "id": "log_full_name",
                        "placeholder": "Your password"
                })

    )
    email = forms.EmailField(
        widget=forms.EmailInput(
                attrs={
                    "class": "form-control",
                        "id": "log_full_name",
                        "placeholder": "Your email"
                })

    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail")
        return email
