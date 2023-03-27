from django.db import models
from seller.models import *
# Create your models here.

class Buyer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pic = models.FileField(default='default.png',upload_to='buyer_profile')

    def __str__(self) -> str:
        return self.first_name
    
class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.buyer)
    
class ViewOrders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    time = models.TimeField(auto_now_add=True)
    date = models.DateField( auto_now_add=True)

    def __str__(self) -> str:
        return str(self.buyer)

    

