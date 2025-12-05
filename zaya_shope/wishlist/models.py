from django.db import models
from zaya_app.models import User

from admin_app.models import Products 

# Create your models here.
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    added_a = models.DateTimeField(auto_now_add=True)

