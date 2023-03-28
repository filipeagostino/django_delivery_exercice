from django import forms

from .models import Shipping

class ShippingForm(forms.ModelForm):

    class Meta:
        model = Shipping
        fields = ('receiver', 'customer', 'product', 'delivery_status', 'deadline', 'price')