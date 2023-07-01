from django.shortcuts import render
from .models import *
from Cart.models import Cart_items
# Create your views here.
from django.db.models import Q

def menu(request):       
    user = request.user.username
    print(user)
    products = Menu.objects.all()

    cart_items = Cart_items.objects.filter(user = user)
    
    print(len(cart_items))
    if len(cart_items) > 0:
        for itm in cart_items:
            filter_products = Menu.objects.filter(item_name__contains=itm)
            if filter_products.exists():
                print('yes exists')
                cart_item = Cart_items.objects.get(
                    Q(user = user)&
                    Q(item = itm )
                )

                filter_products.update(in_cart=True, quantity=cart_item.quantity)
            else:
                print('no exists 1')
                filter_products.update(in_cart=False, quantity=0)
    else:
        filter_products = Menu.objects.all()
        print('no exists 2')
        for itm in filter_products:
            item = Menu.objects.get(item_name = itm)
            item.in_cart = False
            item.quantity = 0
            item.save()

            

            

    context = {'menu_items': products, 'cart': cart_items}
    return render(request,'menu.html', context)

