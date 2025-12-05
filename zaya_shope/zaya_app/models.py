from django.db import models
from django.contrib.auth.models import AbstractUser
from admin_app.models import Products
from admin_app.models import Category

# Create your models here.
class User(AbstractUser):
   
    email = models.EmailField(unique=True)
    phone = models.CharField( max_length=50, unique=True)
    # address = models.TextField(null=True, blank=True)
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["username"] 
    def __str__(self):
        return self.username



