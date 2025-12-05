from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/',blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return self.name

class Products(models.Model):
    
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category,on_delete=models. CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) 
    stock = models.PositiveIntegerField(default=0)
    def __str__(self):
       return self.name
    







