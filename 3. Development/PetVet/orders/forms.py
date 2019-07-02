from django import forms
from django.forms import ModelForm, Textarea, TextInput

from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address','cc_number', 'cc_expiry', 'cc_code']
        # address = {
        #     'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        # }
    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget = TextInput(attrs={'autofocus': 'true', 'class': "s-text7 size1 p-l-23 p-r-50", 'placeholder': "Enter Shipping Address. i.e. Reconquista 631, C1003ABM CABA"})
        self.fields['cc_number'].widget = TextInput(attrs={'autofocus': 'true', 'class': "s-text7 size1 p-l-23 p-r-50", 'placeholder': "0000000000000000"})
        self.fields['cc_expiry'].widget = TextInput(attrs={'autofocus': 'true', 'class': "s-text7 size1 p-l-23 p-r-50", 'placeholder': "MM/YY"})
        self.fields['cc_code'].widget = TextInput(attrs={'autofocus': 'true', 'class': "s-text7 size1 p-l-23 p-r-50", 'placeholder': "CC Validation"})