from django.shortcuts import render,redirect
from Menu.models import *
from Cart.models import *
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
import json
import datetime
from .utils import *
import razorpay
# Create your views here.


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def update_cart(request):
    item_id = request.POST.get('item')
    action = request.POST.get('act')
    print('item_id:', item_id, 'action:', action)

    item = Menu.objects.get(id = item_id)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    cartItem, created = Cart_items.objects.get_or_create(order = order, item = item)

    if action == 'add':
        update_quantity = cartItem.quantity + 1
        cartItem.quantity = update_quantity
        cartItem.save()
    elif action == 'subtract':
        update_quantity = cartItem.quantity - 1
        cartItem.quantity = update_quantity
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
    


def AnonymousUser_cart(request):
    item_id = request.POST.get('item')
    action = request.POST.get('act')

    print('item_id:', item_id, 'action:', action)

    item = Menu.objects.get(id = item_id)  

    item_cookie = request.COOKIES.get('cart')

    

    if item_cookie:
        list = json.loads(item_cookie)
        
        if list != []:
            x = 0
            for item in list:
                x += 1
                print(item)
                if item['item'] == item_id:
                    quantity = item['quantity']
                    if action == 'add':
                        item['quantity'] = quantity + 1
                    
                    elif action == 'subtract':
                        item['quantity'] = quantity - 1
                    
                    elif action == 'remove':
                        list.remove(item)    
                    break
                else:
                    if x < len(list):
                        continue
                    else:
                        list.append({'item': item_id, 'quantity': 1})
                        break
        else:
           list.append({'item': item_id, 'quantity': 1})

                
    else:
        list = [
            {'item': item_id, 'quantity': 1}
        ]
    
    list = json.dumps(list)
    response = HttpResponse('list added')
    response.set_cookie('cart', list)
    return response




def remove_cart_item(request, id):
    customer = request.user.customer
    
    item = Menu.objects.get(id = id)
    order = Order.objects.get(customer = customer, complete = False)
    cart_item = Cart_items.objects.get(order = order, item = item)

    
    cart_item.delete()
        
    if request.GET.get('title')== 'Cart':
        return redirect('/cart/')
    else:
        return redirect('/menu/')
    


def cart(request):
    data = cartData(request)
    order = data['order']
    items = data['items']

    context = {
        'title': 'Cart',
        'items': items,
        'order': order
    }

    
    
    return render(request, 'cart.html', context)


from django.conf import settings
def checkout(request):
    data = cartData(request)
    order = data['order']
    items = data['items']
    option = data['option']
    payment = data['payment']


    context = {
        'title': 'Checkout',
        'items': items,
        'order': order,
        'option': option,
        'payment': payment
    }
    return render(request, 'checkout.html', context)

def payment_success(request):

    data = json.loads(request.body)

    order_id = data['payment_info']['razorpay_order_id']
    payment_id = data['payment_info']['razorpay_payment_id']
    signature = data['payment_info']['razorpay_signature']
    

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(razorpay_order_id=order_id, complete=False)
        order.razorpay_payment_id = payment_id
        order.razorpay_payment_signature = signature
        order.complete = True
        order.save()

    else:
        customer,order = guestOrder(request, data)
    
    send_success_mail(customer,order)

    if data['option'] == 'delivery':
        Delivery_address.objects.create(
            customer=customer,
            order=order,
            address = data['delivery']['address'],
            city = data['delivery']['city'],
            state = data['delivery']['state'],
            pincode = data['delivery']['pincode'],
        ) 
    if data['option'] == 'dinning':
        Dinning_info.objects.create(
            customer = customer,
            order=order,
            phone = data['dinning']['phone'],
            people = data['dinning']['people'],
            date = data['dinning']['date'],
            time = data['dinning']['time'],
            special_req = data['dinning']['special_req'],
        )     

    
    del request.session['cart']
    response =  JsonResponse('payment received', safe=False)
    response.delete_cookie('cart')
    return response