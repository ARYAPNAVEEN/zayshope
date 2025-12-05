from django.shortcuts import render,redirect
from cart_app.models import OrderItems,Order,CartItem,Cart,ShippingAddress
from admin_app.models import Products,Category
from zaya_app.models import User
from discount_app.models import Discount
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
@login_required
def cart(request):
    try:
        cart=Cart.objects.get(user=request.user)

        print(cart.total, cart.exact_total)
        cart_items=CartItem.objects.filter(cart=cart) 
    except:
        pass
    return render(request,'user/cart.html',locals())

@login_required(login_url='login')
def addto_cart(request,id):
    if not request.user.is_authenticated:
        return redirect('shop')

    # Get the product
    product = Products.objects.get(id=id)
    
    #  Choose the price (discount or normal price)
    try:
        discount = product.discount
        if discount and discount.active:
            price = discount.discount_price
        else:
            price = product.price
    except:
        price = product.price

    #  Get or create cart for the user
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    #  Add original product price to exact_total
    cart.exact_total += product.price
    cart.save()

    #  Add product to cart or increase quantity
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.qnty += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, qnty=1)

    #  Update subtotal using discount price
    cart_item.subtotal = cart_item.qnty * price
    cart_item.save()

    # Recalculate cart.total (amount user pays)
    total = 0
    all_items = CartItem.objects.filter(cart=cart)
    for item in all_items:
        total += item.subtotal
        

    cart.total = total
    
    # Calculate savings
    cart.saving = cart.exact_total - cart.total
    cart.save()

    return redirect("cart")

def remove_cart(request, id):
    # Get the cart item to delete
    cart_item = CartItem.objects.get(id=id)
    cart = Cart.objects.get(user=request.user)
    product = cart_item.product
    qnty = cart_item.qnty
    # Calculate subtotal of that cart item
    if product.discount and product.discount.active:
        item_subtotal= qnty*product.discount_price

    else:
         item_subtotal = cart_item.qnty * cart_item.product.price

    # Update cart totals
    cart.total -= item_subtotal               
    cart.exact_total -= item_subtotal
    cart.saving = cart.exact_total - cart.total
    cart.number_of_items -= qnty 
    print(qnty)  
    print(cart.number_of_items)
    # Save the cart
    cart.save()
    # Delete the cart item
    cart_item.delete()

    return redirect('cart')

@require_POST
def update_qnty(request,id):
    cart_item=CartItem.objects.get(id=id)
    cart=cart_item.cart
    product=cart_item.product
    action = request.POST.get("action")
    if action == "increment":
        cart_item.qnty += 1
        cart_item.subtotal = cart_item.qnty * product.price
        cart.exact_total += product.price
        cart.total += product.price   
        cart_item.save()

    elif action == "decrement":
        if cart_item.qnty > 1:
            cart_item.qnty -= 1
            cart_item.subtotal = cart_item.qnty * product.price
            cart.exact_total -= product.price
            cart.total -= product.price   
            cart_item.save()
        else:
            cart.total -= cart_item.subtotal
            cart_item.delete()
    cart.save()
    return redirect("cart")
          

        #    checkout
@login_required
def checkout(request, id=None):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    addresses = ShippingAddress.objects.filter(user=request.user)
    payment_methods = Order.PAYMENT_METHODS
    if request.method == "POST":
        address = request.POST.get("address")
        shipping_address = ShippingAddress.objects.get(id=address)
        
        payment_method = request.POST.get("payment_method")
        print(payment_method)
        total = cart.total
        order=Order.objects.create(
            user = request.user,
            address = shipping_address,
            payment_method=payment_method,
            total=total,
            # status="ordered",
            
        )
        for item in cart_items:

            qnty=item.qnty
            product=item.product
            price=item.subtotal
            OrderItems.objects.create(
                order=order,
                product=product,
                qnty=qnty,
                price=price
            )
        cart.delete()
        print(cart)
        return redirect('success')

    return render(request, 'user/checkout.html', locals())

def success(request):
    return render(request,'user/order_success.html')
    
def add_address(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    # addresses = ShippingAddress.objects.filter(user=request.user)
    payment_methods = Order.PAYMENT_METHODS
    if request.method == "POST":
            main_address = request.POST.get("main_address")
            city = request.POST.get("city")
            # print(main_address,city)
            state = request.POST.get("state")
            pincode = request.POST.get("pincode")
            phone = request.POST.get("phone")

            ShippingAddress.objects.create(
                user=request.user,    
                main_address=main_address,
                city=city,
                state=state,
                pincode=pincode,
                phone=phone
            )
            
            return redirect('checkout')

def edit_address(request,id):
    address=ShippingAddress.objects.get(id=id)
    if request.method == "POST":
            address.main_address = request.POST.get("main_address")
            address.city = request.POST.get("city")
            address.state = request.POST.get("state")
            address.pincode = request.POST.get("pincode")
            address.phone = request.POST.get("phone")
            address.save()
            return redirect('checkout')
    return render(request, 'user/edit_address.html',locals())
            





@login_required
def delete_address(request,id):
    address=ShippingAddress.objects.get(id=id)
    address.delete()
    return redirect('checkout')

def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    # addresses = ShippingAddress.objects.all()
    payment_methods = Order.payment_methods
    if request.method == "POST":
        address=request.POST.get("address")
        print(address)
        payment_method=request.POST.get("payment_method")
        order=Order.objects.create(
            address=address,
            total=cart.total,
            payment_status="pending",
            status="ordered",
            payment_method="payment_method"
          
        )
    for item in cart_items:
        OrderItems.objects.create(
            order=order,
            product=item.product,
            qnty=item.qnty,
            price=item.subtotal
        )
        cart_items.delete()
        cart.total = 0
        cart.exact_total = 0
        cart.saving = 0
        cart.number_of_items = 0
        cart.save()
        
    return redirect('checkout')
       
@login_required
def my_order(request):
    expected_delivery = date.today() + timedelta(days=7)
    order=Order.objects.filter(user=request.user)
    print(order)
    
    return render(request,'user/my_order.html',locals()) 

@login_required
def cancel_order(request,id):
    order=Order.objects.get(id=id,user=request.user)
    order.status = "Cancelled"  
    order.save()
    return redirect('my_order')
 
@login_required
def order_summary(request,id):
    order=Order.objects.get(id=id,user=request.user)
    expected_delivery = date.today() + timedelta(days=7)
    address=order.address
    order_items=OrderItems.objects.filter(order=order)
    steps = ["ordered", "Processing", "Shipped", "Delivered"]
    current_index = steps.index(order.status) if order.status in steps else -1


    return render(request,'user/order_summary.html',locals()) 




def invoice_pdf(request,id):
    order = Order.objects.get(id=id, user=request.user)
    items = OrderItems.objects.filter(order=order)
    template_path = 'user/invoice_pdf.html'
    context = {'order': order, 'items': items}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response
 



