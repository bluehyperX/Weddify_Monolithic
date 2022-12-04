from re import T
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.auth.models import User
from orders.models import Order
from .models import Vendor
from services.models import Service

# Create your views here.



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Something went wrong !')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        is_vendor = request.POST.get('is_vendor')
        service_type = request.POST.get('service_type')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    user.save()
                    messages.success(request, 'You are registerd successfully! ')
                    if is_vendor:
                        vendor = Vendor.objects.create(user=user, service_type=service_type)
                        vendor.save()
                        messages.success(request, 'You are registerd as vendor successfully! ')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')
    


def dashboard(request):
    vendors = Vendor.objects.filter(user=request.user.id)
    states = Service.objects.values_list('state', flat=True).distinct()
    if vendors:
        is_vendor = True
        vendor = vendors[0]
        payments = Order.objects.order_by('-created_date').filter(vendor_id=request.user.id)
        for payment in payments:
            user = User.objects.get(id=payment.user_id)
            setattr(payment, 'user', user)
    else:
        is_vendor = False
        vendor = None
        payments = Order.objects.order_by('-created_date').filter(user_id=request.user.id)
        for payment in payments:
            vendor = User.objects.get(id=payment.vendor_id)
            setattr(payment, 'vendor', vendor)
    data = {
        'payments' : payments,
        'is_vendor': is_vendor,
        'states' : states,
        'vendor' : vendor,
    }
    return render(request, 'accounts/dashboard.html', data)

def profile(request):
    vendors = Vendor.objects.filter(user=request.user.id)
    states = Service.objects.values_list('state', flat=True).distinct()
    if vendors:
        is_vendor = True
        vendor = vendors[0]
        payments = Order.objects.order_by('-created_date').filter(vendor_id=request.user.id)
        for payment in payments:
            user = User.objects.get(id=payment.user_id)
            setattr(payment, 'user', user)
            payment.amount = payment.amount*0.9
    else:
        is_vendor = False
        vendor = None
        payments = Order.objects.order_by('-created_date').filter(user_id=request.user.id)
        for payment in payments:
            vendor = User.objects.get(id=payment.vendor_id)
            setattr(payment, 'vendor', vendor)
    data = {
        'payments' : payments,
        'is_vendor': is_vendor,
        'states' : states,
        'vendor' : vendor,
    }
    return render(request, 'accounts/profile.html', data)

def update_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('profile')
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')

        try:
            user = User.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            if password != None and password != "":
                user.set_password(password)
            auth.login(request, user)
            messages.success(request, "Profile Updated Successfully")
            user.save()
            return redirect('profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('profile')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        # messages.success(request, 'You are successfully logged out !')
        return redirect('home')
    return redirect(request, 'home')

def delete_profile(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('profile')
    else:
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            messages.success(request, "Profile deleted successfully.")
            return redirect('home')
        except:
            messages.error(request, "Failed to Delete Profile")
            return redirect('profile')