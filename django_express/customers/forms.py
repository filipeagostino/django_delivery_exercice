from django import forms

from .models import Customer

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'zip_code', 'address',
        'city', 'district', 'cpf', 'house_number', 'email', 'phone')