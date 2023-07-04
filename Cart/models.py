from django.db import models
from django.contrib.auth.models import User
from Menu.models import *


# Create your models here.


class Cart_items(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, related_name='item', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.item.item_name} {self.user.username}'
    
    class Meta:
        unique_together = ['user', 'item']
    

