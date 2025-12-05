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

from zaya_app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('get_productdetails/<int:id>/',views.get_productdetails,name='get_productdetails'),
    path('get_category',views.get_category,name='get_category'),
    path('product_details/<int:id>/',views.product_details,name='product_details'),
    path('shop/',views.shop,name='shop'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path("reset_password/", views.reset_password, name="reset_password"),
    path('logout_user/',views.logout_user,name='logout'),
    path('account/',views.account,name='account'),
    
   
]
