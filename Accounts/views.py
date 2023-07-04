from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .utils import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from Cart.models import *

# Create your views here.



def register(req):
    if req.method == 'POST':
        first_name = req.POST.get('first_name')
        last_name = req.POST.get('last_name')
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')

        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(req, 'Username already taken')
            return redirect('/register/')
        
        send_email_to_user(username,email)        
        user = User.objects.create(first_name = first_name, last_name = last_name,  username = username, email = email, is_active = False)
        user.set_password(password)
        user.save()
        
        req.session['purpose'] = 'register'
        messages.info(req, 'Otp sent to you email successfully. Please check your email address')
        return redirect("/otp?username="+username)

    return render(req, 'register.html', {'title': 'Register'})

    # return render(request,'register.html')



def login_page(req):

    
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        #User availability check 
        if not User.objects.filter(username = username).exists():
            messages.info(req, 'Invalid username')
            return redirect('/login/')
        

        # is user active
        queryset = User.objects.get(username = username)
        if queryset.is_active != True:
            messages.error(req, 'Your account is not verified, please enter the otp to verify your account')
            send_email_to_user(username, queryset.email)


            return redirect('/otp?username='+ username)

        # password check
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(req, 'Invalid password')
            return redirect('/login/')       
        else:
            login(req, user)
            uptaded_cart = Cart_items.objects.filter(user = req.user.id)
            req.session['cart'] = len(uptaded_cart)
        
            print('length of cart' + str(req.session['cart']))
            return redirect('/menu/')
    
    if req.user.is_authenticated:
        print("You must be logged in")

        return redirect('/')
    
    if req.user:
        uptaded_cart = Cart_items.objects.filter(user = req.user.id)
        req.session['cart'] = len(uptaded_cart)
        
        print('length of cart' + str(req.session['cart']))
    else:
        req.session['cart'] = 0

    return render(req, 'login.html', {'title': 'Login'})



def forget_pass(req):
    if req.method == 'POST':
        user = req.POST.get('user')

        queryset = User.objects.filter(
            Q(username = user)|
            Q(email = user)
        )

        print(queryset)

        if not queryset.exists():
            messages.error(req, 'User does not exist')
            return redirect('/forget-password')

        user_obj = User.objects.get(
            Q(username = user)|
            Q(email = user)
        )
        send_email_to_user(user_obj.username, user_obj.email)
        req.session['purpose'] = 'forget'
        messages.success(req, 'otp sent successfully to email ')
        return redirect("/otp?username="+ user)
    
    return render(req, 'forget_pass.html')



def otp_verify(req): 

    if req.method == 'POST':
        user = req.POST.get('user')
        input_otp = req.POST.get('otp')
        queryset = otp.objects.get(user = user)
        
        original_otp = queryset.otp_no
        print(original_otp)
        if input_otp != original_otp:
            messages.error(req, 'Otp incorrect')
            return redirect('/otp?username='+user)
        
        queryset2 = User.objects.get(username = user)
        queryset2.is_active = True
        queryset2.save()
        queryset.delete()
        if req.session.get('purpose') == 'register':
            messages.success(req, 'Resgistration successful')
            return redirect('/login/')
        
        if req.session.get('purpose') == 'forget':
            req.session['user'] = user
            messages.info(req, 'Creat new password')
            return redirect('/change-password/')
        

    username = req.GET.get('username')
    return render(req, 'otp.html',{'username':username})


def change_password(req):
    if req.method == 'POST':
        user = req.session.get('user')
        user_obj = User.objects.get(username = user)
    
        password = req.POST.get('password')
        cnf_password = req.POST.get('cnf_password')

        if password != cnf_password:
            messages.error(req, 'Password not matching')
            req.session['user'] = user
            return redirect('otp/change-password')
        
        user_obj.set_password(password)
        user_obj.save()
        messages.success(req, 'Password changed successfully')
        return redirect('/login/')
    
    return render(req, 'change_password.html')




    

def logout_page(req):
    logout(req)
    return redirect('/')

def profile(request):
    return render(request,'profile.html')

def update_profile(request):
    return render(request,'update_profile.html')

def edit_booking(request):
    return render(request,'edit_booking.html')

