"""
URL configuration for Restoran project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from home.views import *
from Menu.views import *
from Cart.views import *
from Accounts.views import *

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('service/', services, name='services'),
    path('menu/', menu, name='menu'),
    path('booking/', booking, name='booking'),
    path('team/', team, name='team'),
    path('testimonial/', testimonial, name='testimonial'),
    path('login/', login_page, name='login_page'),
    
    
    path('register/', register, name='register'),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_page),
    path('profile/', profile, name='profile'),
    path('update_profile/', update_profile, name='update_profile'),
    path('edit_booking/', edit_booking, name='edit_booking'),
    path('additional/', additional, name='additional'),
    path('extra/', extra, name='extra'),
    path('otp/', otp_verify,  name='otp'),
    path('forget-password/', forget_pass,  name='forget_pass'),
    path('change-password/', change_password,  name='change_password'),
    path('forget-password-user/', forger_password_user,  name='forger_password_user'),


    path('cart/', cart, name='cart'),
    path('update-cart/', update_cart, name='update_cart'),
    path('anonymousUser-cart/', AnonymousUser_cart, name='anonymousUser_cart'),
    path('cart/remove/<id>', remove_cart_item, name='remove_cart_item'),
    path('checkout/', checkout , name='checkout'),
    path('checkout/success/', payment_success , name='payment_success'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),