from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class otp(models.Model):
    otp_no = models.CharField(max_length=200)
    user = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.otp_no


