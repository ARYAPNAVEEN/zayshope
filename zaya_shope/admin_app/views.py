from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from django.contrib.auth import authenticate,login,logout
from .models import Products
from .models import Category 
from cart_app.models import Order,OrderItems
from zaya_app.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

def dashboard(request):
    total_sales = OrderItems.objects.aggregate(total=Sum('qnty'))['total'] or 0

    # Total Revenue (only delivered orders)
    total_revenue = Order.objects.filter(status="Delivered").aggregate(
        total=Sum('total')
    )['total'] or 0

    # Total Orders
    total_orders = Order.objects.count()

    # Total Customers
    total_customers = User.objects.filter(is_staff=False).count()

    # Pending Orders
    pending_orders = Order.objects.exclude(status__in=["Delivered", "Cancelled"]).count()

    # Cancelled Orders
    cancelled_orders = Order.objects.filter(status="Cancelled").count()

    # Refund Requests — no field in model
    refund_requests = 0

    # Low Stock
    low_stock = Products.objects.filter(stock__lt=10).count()
    
    return render(request,'admin/dashboard.html',locals())


def products(request):
    products = Products.objects.all()
    categorys = Category.objects.all()
    print(categorys)

    return render(request,'admin/products.html',locals())


    
def add_product(request):
    categorys = Category.objects.all()
    print(categorys)
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')  
        image = request.FILES.get('image')
        stock = request.POST.get('stock')
        
        
        try:
            cat = Category.objects.get(id=category_id) 
            print(cat)
            Products.objects.create(
                name=name,
                price=price,
                description=description,
                category=cat,
                image=image,
                stock=stock
            )
            
            return redirect('products')
        except Category.DoesNotExist:
            print(" Category not found")
    
    return render(request, 'admin/add_product.html', {'categorys': categorys})



def get_product(request,id):
    product=Products.objects.get(id=id)
    return redirect('update', id=id)


def edit(request, id):
    product = Products.objects.get(id=id)
    categorys = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')
        category_id = request.POST.get('category')
        product.category = Category.objects.get(id=category_id)
        product.stock = request.POST.get('stock')
        print("PRODUCT CATEGORY:", product.category) 
        if 'image' in request.FILES:
            product.image = request.FILES.get('image')
        product.save()
        return redirect('products')  
    choices=categorys
    return render(request, 'admin/edit.html', locals())

def delete(request,id):
    product=Products.objects.get(id=id)
    product.delete()
    return redirect('products')

def single_product(request,id):
    product=Products.objects.get(id=id)
    return render(request,'admin/single_product.html',locals())

    # category
def category(request):
    categ = Category.objects.all()
    return render(request,'admin/category.html',locals())


def category_view(request,id):
    category=Category.objects.get(id=id)
    products=Products.objects.filter(category=category)
    return render(request,'admin/category_view.html',locals())
def add_categ(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        image=request.FILES.get('image')
        print(image)
        categ=Category.objects.create(name=name,image=image)
        return redirect('category')
    return render(request,'admin/category.html',locals())



def get_categ(request,id):
    categ=Category.objects.get(id=id)
    return render(request, 'admin/category.html',locals())


def edit_categ(request,id):
    categ=Category.objects.get(id=id)
    if request.method == 'POST':
        categ.name=request.POST.get('name')
        if 'image' in request.FILES:
          categ.image=request.FILES.get('image')
        categ.save()
        return redirect('category')
    return render(request,'admin/categ_edit.html',locals())

def delete_categ(request,id):
    categ=Category.objects.get(id=id)
    categ.delete()
    return redirect('category')

@user_passes_test(lambda u: u.is_superuser)
def staff(request):
    staff_users = User.objects.filter(is_staff=True)
    return render(request,'admin/staff.html',locals())

@user_passes_test(lambda u: u.is_superuser)
def add_staff(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        exist_user =User.objects.filter(Q(email=email)|Q(phone=phone))
        if not exist_user:
            user = User.objects.create(username=name,email=email,phone=phone)
            user.set_password(password)
            user.is_staff = True
            user.save()
            return redirect('staff')


        
    return render(request,'admin/add_staff.html')

@user_passes_test(lambda u: u.is_superuser)
def edit_staff(request,id):
    user=User.objects.get(id=id)
    print(user)
    if request.method == "POST":
        
        user.username=request.POST.get('name')
        user.email=request.POST.get('email')
        user.phone=request.POST.get('phone')
        print(user.username)
        user.save()
        return redirect('staff')

    return render(request,'admin/edit_staff.html',locals())

@user_passes_test(lambda u: u.is_superuser)
def delete_staff(request,id):
    user=User.objects.get(id=id)
    user.delete()
    return redirect('staff')

def staff_status(request,id):
    user=User.objects.get(id=id)
    if user.is_active :
        user.is_active=False
        user.save()
    else:
        user.is_active=True
        user.save()
      
    
    return redirect('staff')


def customers(request):
    customers = User.objects.filter(is_staff=False,is_superuser=False)

    return render(request,'admin/customers.html',locals())


@user_passes_test(lambda u: u.is_superuser)
def customer_edit(request,id):
    cust=User.objects.get(id=id)
    print(cust)
    if request.method == "POST":
        
        cust.username=request.POST.get('name')
        cust.email=request.POST.get('email')
        cust.phone=request.POST.get('phone')
        print(cust.username)
        cust.save()
        return redirect('customers')
    return render(request,'admin/customer_edit.html',locals())


def customer_status(request,id):
    user=User.objects.get(id=id)
    if user.is_active :
        user.is_active=False
        user.save()
    else:
        user.is_active=True
        user.save()
    return redirect('customers')
