from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .models import Products
from .models import Category

from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from admin_app.models import Category 
from discount_app.models import Discount

from cart_app.models import OrderItems,ShippingAddress
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart_app.models import Order
from wishlist.models import Wishlist
from discount_app.models import Discount



def custom_404(request, exception):
    return render(request, 'user/404.html')

# Create your views here.
@never_cache
def index(request):
    products = Products.objects.all()
    categorys = Category.objects.all()
    discount = Discount.objects.all()

    return render(request,'user/index.html',locals())


def about(request):
    return render(request,'user/about.html')


def contact(request):
    return render(request,'user/contact.html')


def product_details(request, id):
    product = Products.objects.get(id=id)
    
    discount = Discount.objects.all()
    category = product.category
    related_products = Products.objects.filter(category=category)
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        wishlist_items = [] 
    return render(request, 'user/shop_single.html',locals())


def shop(request):
    products = Products.objects.all()
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        wishlist_items = [] 
    categ = Category.objects.all()
    print(wishlist_items)
    query = request.GET.get('search')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(price__icontains=query)
        )
    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)
    return  render(request,'user/shop.html',locals())


def get_category(request):
    categ = Category.objects.all()
    return redirect('get_category')

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(password,name,email)
        exist_user =User.objects.filter(Q(email=email)|Q(phone=phone))
        if not exist_user:
            user = User.objects.create(username=name,email=email,phone=phone)
            user.set_password(password)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('index')
        # else:
        #     messages.error(request,"user already exist")
        #     return redirect('index')
    return render(request,'user/index.html')
@never_cache
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)

        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            if user.is_superuser or user.is_staff:
                print(user)
                login(request,user)
                print("loggedin")
                messages.success(request, "Welcome back, Admin!")
                return redirect('dashboard')
            else:
                
                login(request,user)
                messages.success(request, f"Welcome {user.username}!")
                return redirect('index')
        else:
            messages.error(request,"invalid email and password")
    return  render(request,'user/index.html')



def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        new_password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)   
            user.set_password(new_password)        
            user.save()

            messages.success(request, "Password reset successful!")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "Email does not exist!")
            return redirect("reset_password")

    return render(request, "user/reset_password.html")

def logout_user(request):
    logout(request)
    return redirect('index')

def get_productdetails(request,id):
    product=Products.objects.get(id=id)
    related_products = Products.objects.filter(category=product.category)
    
    print(related_products)
    print(product.category)
    print(product)
    
    return render(request, 'user/shop_single.html',locals())
   
def get_categ(request,id):
    categ=Category.objects.get(id=id)
    print(categ.name)
    return render(request, 'admin/category.html',locals())


def account(request):
    user = User.objects.get(id=request.user.id)
    address = ShippingAddress.objects.filter(user=request.user).last()
    return render(request,'user/account.html',locals())







