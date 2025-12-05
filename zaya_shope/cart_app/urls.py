"""
URL configuration for zaya_shope project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from cart_app import views

urlpatterns = [

    path('cart/',views.cart,name='cart'),
    path("checkout/", views.checkout, name="checkout"),  
    path("add_address/",views.add_address,name="add_address"),
    path('place_order/',views.place_order,name="place_order"),
    path('addto_cart/<int:id>/',views.addto_cart,name="addto_cart"),
    path('edit_address/<int:id>/',views.edit_address,name="edit_address"),
    path('delete_address/<int:id>',views.delete_address,name="delete_address"),
    path('remove_cart/<int:id>/',views.remove_cart,name="remove_cart"),
    path('update_qnty/<int:id>/',views.update_qnty,name="update_qnty"),
    path('success/',views.success,name="success"),
    path('my_order/',views.my_order,name="my_order"),
    path('cancel_oder/<int:id>/',views.cancel_order,name="cancel_order"),
    path('order_summary/<int:id>/',views.order_summary,name="order_summary"),
    path("invoice/<int:id>/download/", views.invoice_pdf, name="invoice_pdf"),

    
    
   
]
