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

from admin_app import views

urlpatterns = [
    
    path('dashboard/',views.dashboard,name='dashboard'),
    path('products/',views.products,name='products'),
    path('add_product/',views.add_product,name='addproduct'),
    path(' get_product/<int:id>/',views. get_product,name= 'get_product'),
    path('update/<int:id>/', views.edit, name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('single_product/<int:id>/',views.single_product,name='single_product'),
    path('category/',views.category,name='category'),
    path('category_view/<int:id>/',views.category_view,name='category_view'),
    path('get_categ/<int:id>/',views.get_categ,name='get_categ'),
    path('add_categ/',views.add_categ,name='add_categ'),
    path('edit_categ/<int:id>/',views.edit_categ,name='categ_edit'),
    path('delete_categ/<int:id>/',views.delete_categ,name='delete_categ'),
    path('staff/',views.staff,name='staff'),
    path('add_staff/',views.add_staff,name='add_staff'),
    path('edit_staff/<int:id>/',views.edit_staff,name='edit_staff'),
    path('delete_staff/<int:id>/',views.delete_staff,name='delete_staff'),
    path('staff_status/<int:id>/',views.staff_status,name='staff_status'),
    path('customers/',views.customers,name='customers'),
    path('customer_edit/<int:id>/',views.customer_edit,name='customer_edit'),
    path('customer_status<int:id>/',views.customer_status,name='customer_status'),

   
]
