from django.db import models
from zaya_app.models import User
from admin_app.models import Products
from discount_app.models import Discount


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    exact_total = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    saving = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    number_of_items = models.IntegerField(default=1)


class CartItem(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE) 
    qnty = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8,decimal_places=2,default=0)

class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    main_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone = models.CharField( max_length=50, unique=True, null=False, blank=False)

class Order(models.Model):
    
    STATUS = [
        ("ordered", "ordered"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    PAYMENT_METHODS = [
        ("UPI","UPI"),
        ("COD","cash on delivery"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, default="Pending")  
    status = models.CharField(max_length=20, choices=STATUS, default="ordered")
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default="COD")
    
    
    
class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    qnty=models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    

    
            