from django.shortcuts import render
from .models import *
from Cart.models import *
# Create your views here.
from django.db.models import Q

def menu(request):       
    user = request.user.id
    items = Menu.objects.all()



    # cart_items = Cart_items.objects.filter(user = user)
    
    # print(len(cart_items))
    # if len(cart_items) > 0:
    #     for itm in items:
    #         print(itm.item_name)
    #         for c_item in cart_items:

    #             print(c_item.item)
    #             yes_exist = False
    #             if yes_exist == True:
    #                 break
    #             else:
    #                 selected_item = Menu.objects.get(id=c_item.item_id)
    #                 selected_item.in_cart = False
    #                 selected_item.quantity = 0
    #                 selected_item.save()

    #             if itm.id == c_item.item_id:
    #                 print('yes exists')
    #                 yes_exist = True
    #                 selected_item = Menu.objects.get(id=c_item.item_id)
    #                 selected_item.in_cart = True
    #                 selected_item.quantity = c_item.quantity
    #                 selected_item.save()
    # else:
    #     print('no item in cart')    
    #     for itm in items:
    #         item = Menu.objects.get(item_name = itm)
    #         item.in_cart = False
    #         item.quantity = 0
    #         item.save()

            

            

    context = {'title': 'Menu', 'menu_items': items,}
    return render(request,'menu.html', context)

