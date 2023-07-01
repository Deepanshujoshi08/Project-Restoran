from django.db import models

# Create your models here.


class Menu(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    item_price = models.IntegerField()
    item_image = models.ImageField(upload_to="menu_items")
    in_cart = models.BooleanField(default=False)
    quantity = models.IntegerField(blank=True ,default=0)

    def __str__(self) -> str:
        return self.item_name
    
