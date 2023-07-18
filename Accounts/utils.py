from .models import *
from django.core.mail import send_mail
from django.conf import settings
import random



def send_email_to_user(user,email):
    queryset = otp.objects.filter(user = user)

    subject = "Account Verification For Restoran User"
    random_num = random.randint(100000, 999999)
    str_num = str(random_num)
    message = "Your Otp for Restoran account verfication is " + str_num
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    if not queryset.exists():
        mail = otp.objects.create(otp_no=random_num, user=user)
        mail.save()
    
    queryset2 = otp.objects.get(user=user)
    queryset2.otp_no = random_num
    queryset2.save()
    
    



# def orders(user,name):
#         # user_obj = User.objects.all()
#         item = Menu.objects.filter(item_name = name)
#         quantity = 1
#         order = Items.objects.create(name = item, quantity = quantity) 
#         order.save()
#         return order
        
