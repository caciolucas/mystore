from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f'{self.name} (R$ {self.price})'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
