from django.shortcuts import render
from .models import *
from Cart.models import *
# Create your views here.
from django.db.models import Q
from Cart.utils import cart_check

def menu(request):     
    cart_check(request)  
    user = request.user.id
    items = Menu.objects.all()       

    context = {'title': 'Menu', 'menu_items': items}
    return render(request,'menu.html', context)

