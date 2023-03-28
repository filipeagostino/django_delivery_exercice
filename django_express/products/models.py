from django.db import models

from django.contrib.auth import get_user_model


class Product(models.Model):
    # Definindo os campos

    name = models.CharField(max_length=100)
    height = models.DecimalField('Height: (20,00) Cms', max_digits=4, decimal_places=2)
    width = models.DecimalField('Width: (20,00) Cms', max_digits=4, decimal_places=2)
    length = models.DecimalField('Length: (20,00) Cms', max_digits=4, decimal_places=2)
    weight = models.DecimalField('Weight: (11,000) Grams', max_digits=5, decimal_places=3)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)