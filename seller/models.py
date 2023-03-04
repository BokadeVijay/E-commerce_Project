from django.db import models

# Create your models here.
class Seller(models.Model):
    user_name = models.CharField(max_length=50)
    gst = models.CharField(max_length=15)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    pic = models.FileField(default= 'defualt.png',upload_to='seller_profile')

    def __str__(self) -> str:
        return self.user_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    des = models.TextField(max_length=255)
    price = models.FloatField(default=10.0)
    product_stock = models.IntegerField(default=0)
    pic = models.FileField(default='sad.jpg', upload_to='product_pics')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
class MyOrder(models.Model):
    

