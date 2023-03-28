from django.db import models

from django.contrib.auth import get_user_model


class Customer(models.Model):
    # Definindo os campos

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zip_code = models.CharField('Zip Code: (13123123)', max_length=8)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    cpf = models.CharField('Cpf: (12312312312)',max_length=11, unique=True)
    house_number = models.CharField(max_length=5)
    email = models.CharField('Email: (example@example.com.br)', max_length=100)
    phone = models.CharField(max_length=12)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.first_name)
