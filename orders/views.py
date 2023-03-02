import datetime
from datetime import date
from django.utils.timezone import utc
from django.shortcuts import render, redirect
from django.contrib import messages, auth
import requests
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
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        amount = request.POST['amount']
        event_date = request.POST['event_date']
        curr = event_date
        back = date.today()

        if Order.objects.filter(service_id=service_id).exists():
                messages.error(request, 'This service is already booked!')
                return redirect('dashboard')
        
        order = Order(service_id=service_id, title=title, user_id=user_id, vendor_id=vendor_id, first_name=first_name,
        last_name=last_name, city=city, state=state, email=email, phone=phone, 
        amount=amount, event_date=event_date)

        order.save()
        messages.success(request, 'Thankyou for booking. we will get back to you soon !')
        UserDict={"firstname":first_name, "lastname":last_name, "email":email, "username":"", "servicetitle":title}
        r=requests.post('http://localhost:8080/book', json=UserDict)
        return redirect('/services/'+service_id)

def delete_order(request, id):
    order = Order.objects.get(id=id)
    try:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        duration = now - order.created_date
        if duration.total_seconds() > (24*3600):
            messages.error(request, "Orders cannot be canceled after 24 hours !")
            return redirect('dashboard')
        messages.success(request, "Order Canceled successfully.")
        UserDict={"firstname":order.first_name, "lastname":order.last_name, "email":order.email, "username":"", "servicetitle":order.title}
        r=requests.post('http://localhost:8080/cancelbook', json=UserDict)
        order.delete()
        return redirect('dashboard')
    except:
        raise
