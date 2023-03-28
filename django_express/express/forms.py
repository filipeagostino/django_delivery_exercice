from django import forms

from .models import Deliverer

class DelivererForm(forms.ModelForm):

    class Meta:
        model = Deliverer
        fields = ('first_name', 'last_name', 'zip_code', 'address',
        'city', 'district', 'cpf', 'house_number')