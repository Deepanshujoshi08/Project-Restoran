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



def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        
        emailCheck = User.objects.filter(email = email)

        if emailCheck.exists():
            messages.info(request, 'Email already taken')
            return redirect('/register/')
        


        if password != cpassword:
            messages.warning(request, 'Password not matched.')
            return redirect('/register')
        
        send_email_to_user(username,email)        
        user = User.objects.create(first_name = first_name, last_name = last_name,  username = username, email = email, is_active = False)
        user.set_password(password)
        user.save()
        
        request.session['purpose'] = 'register'
        messages.info(request, 'Otp sent to you email successfully. Please check your email address')
        return redirect("/otp?username="+username)

    return render(request, 'register.html', {'title': 'Register'})

    # return render(request,'register.html')



def login_page(request):

    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #User availability check 
        if not User.objects.filter(username = username).exists():
            messages.info(request, 'Invalid username')
            return redirect('/login/')
        

        # is user active
        queryset = User.objects.get(username = username)
        if queryset.is_active != True:
            messages.error(request, 'Your account is not verified, please enter the otp to verify your account')
            send_email_to_user(username, queryset.email)


            return redirect('/otp?username='+ username)

        # password check
        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')       
        else:
            login(request, user)
            
            customer, create = Customer.objects.get_or_create(email = request.user.email)
            customer.user = request.user
            customer.name = request.user.get_full_name()
            print(request.user)
            customer.save()
            updated_cart = Order.objects.filter(customer = request.user.customer, complete = False)
            if updated_cart:
                updated_cart = Order.objects.get(customer = request.user.customer, complete = False)
                request.session['cart'] = updated_cart.get_cart_items        
            return redirect('/menu/')
    
    if request.user.is_authenticated:
        print("You must be logged in")

        return redirect('/')
    
    # if request.user:
    #     uptaded_cart = Order.objects.filter(user = request.user.id)
    #     request.session['cart'] = uptaded_cart.get_cart_items()
        
    #     print('length of cart' + str(request.session['cart']))
    # else:
    #     request.session['cart'] = 0

    return render(request, 'login.html', {'title': 'Login'})



def forget_pass(request):
    if request.method == 'POST':
        user = request.POST.get('user')

        queryset = User.objects.filter(
            Q(username = user)|
            Q(email = user)
        )

        print(queryset)

        if not queryset.exists():
            messages.error(request, 'User does not exist')
            return redirect('/forget-password')

        user_obj = User.objects.get(
            Q(username = user)|
            Q(email = user)
        )
        send_email_to_user(user_obj.username, user_obj.email)
        request.session['purpose'] = 'forget'
        messages.success(request, 'otp sent successfully to email ')
        return redirect("/otp?username="+ user)
    
    return render(request, 'forget_pass.html')

def forger_password_user(request):
    user = request.user.username

    query = User.objects.get(username = user)

    send_email_to_user(user, query.email)
    messages.success(request, 'otp sent successfully to email ')
    return redirect("/otp/?username="+user)




def otp_verify(request): 

    if request.method == 'POST':
        user = request.POST.get('user')
        input_otp = request.POST.get('otp')
        queryset = otp.objects.get(user = user)
        
        original_otp = queryset.otp_no
        print(original_otp)
        if input_otp != original_otp:
            messages.error(request, 'Otp incorrect')
            return redirect('/otp?username='+user)
        
        queryset2 = User.objects.get(username = user)
        queryset2.is_active = True
        queryset2.save()
        queryset.delete()
        if request.session.get('purpose') == 'register':
            messages.success(request, 'Resgistration successful')
            return redirect('/login/')
        
        if request.session.get('purpose') == 'forget':
            request.session['user'] = user
            messages.info(request, 'Creat new password')
            return redirect('/change-password/')
        

    username = request.GET.get('username')
    return render(request, 'otp.html',{'username':username})




def change_password(request):
    if request.method == 'POST':
        user = request.session.get('user')
        user_obj = User.objects.get(username = user)
    
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnf_password')

        if password != cnf_password:
            messages.error(request, 'Password not matching')
            request.session['user'] = user
            return redirect('otp/change-password')
        
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'Password changed successfully')
        return redirect('/login/')
    

    return render(request, 'change_password.html')




    

def logout_page(request):
    logout(request)
    return redirect('/')

def profile(request):
    return render(request,'profile.html')

def update_profile(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        User.objects.get(username = username)
        User.first_name = fname
        User.last_name = lname
        User.email = email
        User.save()

    return render(request,'update_profile.html')

def edit_booking(request):
    return render(request,'edit_booking.html')

