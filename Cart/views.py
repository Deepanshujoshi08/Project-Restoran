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

            uptaded_cart = Cart_items.objects.filter(user = request.user.id)
            request.session['cart'] = len(uptaded_cart)
        
            print('length of cart' + str(request.session['cart']))
            
        return redirect('/menu/')
    
    else:
        return redirect('/login/')


def remove_cart_item(req, id):
    user = req.user
    menu = Menu.objects.get(id = id)
    cart = Cart_items.objects.get(
        Q(user = user)&
        Q(item_id = id)
    )   

    menu.quantity = 0
    menu.in_cart = False
    menu.save()
    cart.delete()
    uptaded_cart = Cart_items.objects.filter(user = req.user.id)
    req.session['cart'] = len(uptaded_cart)
        
    print('length of cart' + str(req.session['cart']))
    if req.GET.get('title')== 'Cart':
        return redirect('/cart/')
    else:
        return redirect('/menu/')
    


def cart(req):

    cart_items = Cart_items.objects.filter(user = req.user.id)
    
    
    return render(req, 'cart.html', {'title': 'Cart', 'cart':cart_items })