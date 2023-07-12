from django.db import models
from django.contrib.auth.models import User
from Menu.models import *
from django.utils.timezone import now



# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    order_option = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return str(self.transaction_id)
    
    @property
    def get_cart_total(self) -> str:
        Cart_items = self.cart_items_set.all()
        total = sum([item.get_total for item in Cart_items])
        return total
    
    @property
    def get_cart_items(self) -> str:
        Cart_items = self.cart_items_set.all()
        total = len([item.quantity for item in Cart_items])
        return total


class Cart_items(models.Model):

    item = models.ForeignKey(Menu, related_name='menu', on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self) -> str:
        total = self.item.item_price * self.quantity
        return total
        
    

class Delivery_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address


class Dinning_info(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    people = models.IntegerField(default=1, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    special_req = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
