from django.contrib import admin
from .models import Cart, CartItem,Order,OrderItems,ShippingAddress

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItems)
admin.site.register(ShippingAddress)
