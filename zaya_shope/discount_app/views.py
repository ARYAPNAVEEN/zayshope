from django.shortcuts import render,redirect
from .models import Discount
from admin_app.models import Products
from decimal import Decimal
from django.contrib import messages

# discount views
def discount(request):
    products = Products.objects.all()
    discounts  = Discount.objects.all()
    return render(request,'admin/discount.html',locals())

def add_discount(request):
    products = Products.objects.all()
    if request.method == 'POST':
        name = request.POST.get("name")
        percentage = Decimal(request.POST.get("percentage"))
        active = request.POST.get("active") == "on"
        product_id = request.POST.get("product")
        product = Products.objects.get(id=product_id)
        if Discount.objects.filter(product=product).exists():
            messages.error(request, "This product already has a discount!")
            return redirect("discount")
        discount_price = product.price - (product.price * (percentage / Decimal(100)))
        Discount.objects.create(
            name = name,
            percentage = percentage,
            discount_price = discount_price,
            active = active,
            product=product,
        )
        messages.success(request, "Discount added successfully!")
       
        return redirect("discount")
    return render(request,'admin/add_discount.html',locals())
      