from django.shortcuts import render,redirect
from Menu.models import *
from Cart.models import *
from django.db.models import Q
# Create your views here.



def add_to_cart(request):
    user = request.user

    if user:
        id = request.POST.get('id') 
        qnt = request.POST.get('quantity')
        menu = Menu.objects.get(id = id)

        cart = Cart_items.objects.filter(
            Q(user = user)&
            Q(item = menu)
        )
        
        if cart.exists():
            # print("Cart already exists")
            # cart = Cart_items.objects.get(user = user , item = menu.item_name)
            cart.update(quantity = qnt)
        else:
            order = Cart_items.objects.create(user = user, item = menu, quantity = qnt) 
            order.save()
        
        
            
        
        return redirect('/menu/')
    
    else:
        return redirect('/login/')
