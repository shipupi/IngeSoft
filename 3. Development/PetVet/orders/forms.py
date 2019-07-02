from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'postal_code',
                'city', 'cc_number', 'cc_expiry', 'cc_code']
