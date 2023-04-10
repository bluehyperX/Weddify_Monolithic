import datetime
from datetime import date, datetime
from django.utils.timezone import utc
from django.shortcuts import render, redirect
from django.contrib import messages, auth
import requests

from services.models import Service
from .models import Order
from django.contrib.auth.models import User


# Create your views here.

def payment(request):
    if request.method == 'POST':

        service_id = request.POST['service_id']
        title = request.POST['title']
        user_id = request.POST['user_id']
        vendor_id = request.POST['vendor_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        amount = Service.objects.get(id=service_id).featured_package_price
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        date_format = "%Y-%m-%d"
        duration = datetime.strptime(end_date, date_format).date()-datetime.strptime(start_date, date_format).date()

        if Order.objects.filter(service_id=service_id).exists():
                messages.error(request, 'This service is already booked!')
                return redirect('dashboard')
        
        if (duration<0):
            messages.error(request, 'Invalid Date Range!')
            return redirect('/services/'+service_id)
        
        order = Order(service_id=service_id, title=title, user_id=user_id, vendor_id=vendor_id, first_name=first_name,
        last_name=last_name, email=email, phone=phone, amount=amount, start_date=start_date, end_date=end_date)

        order.save()
        messages.success(request, 'Thankyou for booking. we will get back to you soon!')
        UserDict={"firstname":first_name, "lastname":last_name, "email":email, "username":"", "servicetitle":title}
        r=requests.post('http://localhost:8080/book', json=UserDict)
        UserDict={"firstname":User.objects.get(id=order.vendor_id).first_name, "lastname":User.objects.get(id=order.vendor_id).last_name, "email":User.objects.get(id=order.vendor_id).email, "username":first_name, "servicetitle":title}
        r=requests.post('http://localhost:8080/bookvendor', json=UserDict)
        return redirect('/services/'+service_id)

def delete_order(request, id):
    order = Order.objects.get(id=id)
    try:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        duration = now - order.created_date
        if duration.total_seconds() > (24*3600):
            messages.error(request, "Orders cannot be canceled after 24 hours!")
            return redirect('dashboard')
        messages.success(request, "Order Canceled successfully.")
        UserDict={"firstname":order.first_name, "lastname":order.last_name, "email":order.email, "username":"", "servicetitle":order.title}
        r=requests.post('http://localhost:8080/cancelbook', json=UserDict)
        UserDict={"firstname":User.objects.get(id=order.vendor_id).first_name, "lastname":User.objects.get(id=order.vendor_id).last_name, "email":User.objects.get(id=order.vendor_id).email, "username":order.first_name, "servicetitle":order.title}
        r=requests.post('http://localhost:8080/cancelbookvendor', json=UserDict)
        order.delete()
        return redirect('dashboard')
    except:
        raise
