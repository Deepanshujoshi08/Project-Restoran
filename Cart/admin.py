from django.contrib import admin
from .models import *
# Register your models here.


class Cart_itemsAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'user']


admin.site.register(Cart_items, Cart_itemsAdmin)