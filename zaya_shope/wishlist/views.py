from django.shortcuts import render,redirect
from .models import Wishlist
from admin_app.models import Products
from zaya_app.models import User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from wishlist import urls
from django.contrib import messages
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request,'user/wishlist.html',locals())

@login_required
def add_to_wishlist(request,id):
    product = Products.objects.get(id=id)
    wishlist_items = Wishlist.objects.filter(user=request.user)
    if product in wishlist_items:
        messages.info(request, "Product already in wishlist")
    else:
        wishlist = Wishlist.objects.create(user=request.user,product=product)
    return redirect(request.META.get("HTTP_REFERER", "/"))

@login_required(login_url='login')
def remove_from_wishlist(request,id):
    wishlist_item = Wishlist.objects.get(user=request.user, product_id=id)
    wishlist_item.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))
