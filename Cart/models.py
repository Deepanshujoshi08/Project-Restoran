from django.db import models

# Create your models here.


class Cart_items(models.Model):
    user = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.item