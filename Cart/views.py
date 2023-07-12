from django.shortcuts import render,redirect
from Menu.models import *
from Cart.models import *
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
import json
import datetime
# Create your views here.


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def update_cart(request):
    item_id = request.POST.get('item')
    action = request.POST.get('act')

    print('item_id:', item_id, 'action:', action)

    user = request.user
    item = Menu.objects.get(id = item_id)

    order, created = Order.objects.get_or_create(user = user, complete = False)

    cartItem, created = Cart_items.objects.get_or_create(order = order, item = item)

    if action == 'add':
        update_qnt = cartItem.quantity + 1
        cartItem.quantity = update_qnt
        cartItem.save()
    elif action == 'subtract':
        update_qnt = cartItem.quantity - 1
        cartItem.quantity = update_qnt
        cartItem.save()
    elif action == 'remove':
        cartItem.delete()


    if cartItem.quantity <= 0:
        cartItem.delete()

    print('order:', cartItem.item, 'here it is')
    # data = [
    #     {'item': order.item, 'quantity': order.quantity}
    # ]

    total_items = order.get_cart_items
    request.session['cart'] = total_items

    print('total_items:', total_items)
    

    data = Object()
    data.item = cartItem.item.item_name
    data.quantity = cartItem.quantity
    data = data.toJSON()

    return JsonResponse(data, safe=False)



def add_to_cart(request):
    user = request.user

    if user:
        id = request.POST.get('item_id', None)
        print('the product id :', id, ' of', user.username)
        qnt = request.POST.get('quantity', None)
        print('the product quantity :', qnt , ' of', user.username)
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
        
        cart = Cart_items.objects.get(
            Q(user = user)&
            Q(item = menu)
        )
        data = {
            'quantity': cart.quantity
        }
        return HttpResponse(data)
    
    else:
        return redirect('/login/')


def remove_cart_item(request, id):
    user = request.user
    
    item = Menu.objects.get(id = id)
    order = Order.objects.get(user = user, complete = False)
    cart_item = Cart_items.objects.get(order = order, item = item)

    
    cart_item.delete()
        
    if request.GET.get('title')== 'Cart':
        return redirect('/cart/')
    else:
        return redirect('/menu/')
    


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete= False)
        items = order.cart_items_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'title': 'Cart',
        'items': items,
        'order': order
    }

    
    
    return render(request, 'cart.html', context)


def checkout(request):
    option = request.GET.get('option')
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete= False)
        order.order_option = option
        order.save()
        items = order.cart_items_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {
        'title': 'Checkout',
        'items': items,
        'order': order,
        'option': option
    }
    return render(request, 'checkout.html', context)


def process_order(request):

    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.order_option == 'delivery':
            Delivery_address.objects.create(
                user=user,
                order=order,
                address = data['delivery']['address'],
                city = data['delivery']['city'],
                state = data['delivery']['state'],
                pincode = data['delivery']['pincode'],
            ) 
        if order.order_option == 'dinning':
            Dinning_info.objects.create(
                user=user,
                order=order,
                name = data['dinning']['name'],
                email = data['dinning']['email'],
                phone = data['dinning']['phone'],
                people = data['dinning']['people'],
                date = data['dinning']['date'],
                time = data['dinning']['time'],
                special_req = data['dinning']['special_req'],
            ) 

    return JsonResponse('payment received', safe=False)