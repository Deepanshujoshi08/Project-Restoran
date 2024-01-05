import json
from django.http import HttpResponse,JsonResponse

from Cart.models import *
from Menu.models import *
import razorpay
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings


def cart_check(request):
    if request.COOKIES.get('cart'):
        cart = json.loads(request.COOKIES.get('cart'))
        if cart == []:
            request.session['cart'] = 0
        else:
            total = 0
            for i in cart:
                total += i['quantity']

            request.session['cart'] = total
    
def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES.get('cart'))           
    except:
        cart = {}
    items = []
    cart_order = {'get_cart_total': 0, 'get_cart_items': 0,}
    Cart_items = cart_order['get_cart_items']
    
    # print(cart)

    for i in cart:
        print(i)
        try:
            # Cart_items += i['quantity']
            item = Menu.objects.get(id = i['item'])
            total = (item.item_price * i['quantity'])

            cart_order['get_cart_total'] += total
            cart_order['get_cart_items'] += i['quantity']

            item = { 
                'item':{
                    'id': item.id,
                    'item_name': item.item_name,
                    'item_price': item.item_price,
                    'item_image': item.item_image,
                },
                'item_id': item.id,
                'quantity': i['quantity'],
                'get_total' : total
            }   
            items.append(item)
        except:
            pass
    
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create({'amount': cart_order['get_cart_total'] * 100, 'currency': 'INR', 'payment_capture': 1})


    return{'items': items, 'order': cart_order, 'payment': payment}



def cartData(request):
    cart_check(request)
    option = request.GET.get('option')


    if request.user.is_authenticated:
        customer = request.user.customer
        cart_order, created = Order.objects.get_or_create(customer=customer, complete= False)
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment = client.order.create({'amount': cart_order.get_cart_total * 100, 'currency': 'INR', 'payment_capture': 1})
        cart_order.razorpay_order_id = payment['id']
        cart_order.order_option = option
        cart_order.save()
        items = cart_order.cart_items_set.all()
    else:
        cookieData = cookieCart(request)
        cart_order = cookieData['order']
        items = cookieData['items']
        payment = cookieData['payment']
   

    return {'items': items, 'order': cart_order, 'option': option, 'payment': payment}


def guestOrder(request, data):
    print('User is not logged in')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    order_id = data['payment_info']['razorpay_order_id']
    payment_id = data['payment_info']['razorpay_payment_id']
    signature = data['payment_info']['razorpay_signature']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, create = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete=True,
        razorpay_order_id = order_id,
        razorpay_payment_id = payment_id,
        razorpay_payment_signature = signature
    )

    for item in items:
        menu_item = Menu.objects.get(id=item['item']['id'])

        Cart_item = Cart_items.objects.create(
            item = menu_item,
            order = order,
            quantity = item['quantity']

        )
    return customer, order



def send_success_mail(customer,order):

    email = customer.email
    name = customer.name
    subject = "Order from Restron"
    
    message = "Dear " + name + ", your order is placed."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    