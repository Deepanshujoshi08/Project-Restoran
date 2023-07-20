from django.contrib import admin
from .models import *
# Register your models here.




class Cart_itemsAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'order']


class Dinning_infoAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'people', 'date', 'time']

class Delivery_addressAdmin(admin.ModelAdmin):
    list_display = ['order', 'customer', 'address']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'complete', 'razorpay_order_id']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Cart_items, Cart_itemsAdmin,)
admin.site.register(Dinning_info, Dinning_infoAdmin)
admin.site.register(Delivery_address, Delivery_addressAdmin)

admin.site.register(Order, OrderAdmin)
