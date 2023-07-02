from django.contrib import admin
from .models import *
# Register your models here.


class MenuAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'item_price']

admin.site.register(Menu, MenuAdmin)
