from django.db import models

from django.contrib.auth import get_user_model

from express.models import Deliverer
from customers.models import Customer
from products.models import Product


class Shipping(models.Model):
    # Definindo os campos

    transport = 'transport'
    delivered = 'delivered'
    
    status = [
        (transport, 'transport'),
        (delivered, 'delivered'),
    ]

    receiver = models.ForeignKey(Deliverer, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=9, choices=status, default=transport)
    deadline = models.PositiveIntegerField('Deadline: (1) Days')
    price = models.DecimalField('Price: (00,00)', max_digits=5, decimal_places=2)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.receiver)