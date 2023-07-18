from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from Cart.utils import cart_check

# Create your views here.


def home(request):
    cart_check(request)
    return render(request,'index.html', {'title': 'Home'})

def about(request):
    cart_check(request)
    return render(request,'about.html', {'title': 'About'})

def services(request):
    cart_check(request)
    return render(request,'service.html', {'title': 'Services'})

def contact(request):
    cart_check(request)
    return render(request,'contact.html', {'title': 'Contact'})





# @login_required(login_url='/login/') 
def booking(request):
    cart_check(request)
    return render(request,'booking.html', {'title': 'Booking'})

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')


def additional(request):
    return render(request,'additional.html')

def extra(request):
    queryset = User.objects.all()
    context = {'user': queryset}
    
    return render(request,'extra.html', context)

