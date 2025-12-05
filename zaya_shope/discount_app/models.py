from django.db import models
from admin_app.models import Products
from admin_app.models import Category

class Discount(models.Model):
    name = models.CharField(max_length=100)   
    percentage = models.PositiveIntegerField(default=0)  
    active = models.BooleanField(default=True)
    discount_price = models.DecimalField(max_digits=10,decimal_places=2)
    # saving = models.DecimalField(max_digit=10,decimal_places=2)
    product = models.OneToOneField(Products,on_delete=models.CASCADE,related_name="discount")
    def __str__(self):
        return self.name
