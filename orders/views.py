import datetime
import json
from datetime import date,datetime
import logging
from django.utils.timezone import utc
from django.shortcuts import render, redirect
from django.contrib import messages
from rabbitmq import email_cancelbook, email_book, email_bookvendor, email_cancelbookvendor
from services.models import Service
from .models import Order
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum

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
        duration = datetime.strptime(end_date, date_format).date()>=datetime.strptime(start_date, date_format).date()

        existing_orders=Order.objects.filter(service_id=service_id)
        
        if user_id==vendor_id:
            messages.error(request, 'Not Allowed to book own service!')
            return redirect('/services/'+service_id)
        elif (not duration):
            messages.error(request, 'Invalid Date Range!')
            return redirect('/services/'+service_id)
        elif existing_orders.exists():
                #MATCH DATES of booked service new new booking
                for ord in existing_orders:
                    if datetime.strptime(start_date, date_format).replace(tzinfo=utc)<=ord.end_date.replace(tzinfo=utc) or datetime.strptime(end_date, date_format).replace(tzinfo=utc)>=ord.start_date.replace(tzinfo=utc):
                        logger = logging.getLogger(__name__)
                        logger.info(datetime.strptime(start_date, date_format).replace(tzinfo=utc))
                        logger.info(ord.end_date.replace(tzinfo=utc))
                        logger.info(datetime.strptime(end_date, date_format).replace(tzinfo=utc))
                        logger.info(ord.start_date.replace(tzinfo=utc))
                        messages.error(request, 'This service is already booked!')
                        # return redirect('home')
                        return redirect('/services/'+service_id)
        
        order = Order(service_id=service_id, title=title, user_id=user_id, vendor_id=vendor_id, first_name=first_name,
        last_name=last_name, email=email, phone=phone, amount=amount, start_date=start_date, end_date=end_date)

        order.save()
        messages.success(request, 'Thankyou for booking. we will get back to you soon!')

        #request paytm to transfer amount
        param_dict= {
                'MID': 'RqWMsL91028787485689',
                'ORDER_ID':str(order.id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/weddify/handlerequest/',
        }

        
        UserDict={"firstname":first_name, "lastname":last_name, "email":email, "username":"", "servicetitle":title}
        email_book(json.dumps(UserDict))

        UserDict={"firstname":User.objects.get(id=order.vendor_id).first_name, "lastname":User.objects.get(id=order.vendor_id).last_name, "email":User.objects.get(id=order.vendor_id).email, "username":first_name, "servicetitle":title}
        email_bookvendor(json.dumps(UserDict))

        paytmChecksum = PaytmChecksum.generateSignature(param_dict, "AlulEP3fgbQClt4w")
        param_dict['CHECKSUMHASH']=paytmChecksum
        return render(request, '../templates/pages/paytm.html', {'param_dict': param_dict})

        return redirect('/services/'+service_id)
        

def delete_order(request, id):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('profile')
    else:
        order = Order.objects.get(id=id)
        try:
            now = datetime.utcnow().replace(tzinfo=utc)
            duration = now - order.created_date
            if duration.total_seconds() > (24*3600):
                messages.error(request, "Orders cannot be canceled after 24 hours!")
                return redirect('dashboard')
            messages.success(request, "Order Canceled successfully.")

            UserDict={"firstname":order.first_name, "lastname":order.last_name, "email":order.email, "username":"", "servicetitle":order.title}
            email_cancelbook(json.dumps(UserDict))

            UserDict={"firstname":User.objects.get(id=order.vendor_id).first_name, "lastname":User.objects.get(id=order.vendor_id).last_name, "email":User.objects.get(id=order.vendor_id).email, "username":order.first_name, "servicetitle":order.title}
            email_cancelbookvendor(json.dumps(UserDict))

            order.delete()
            return redirect('dashboard')
        except:
            raise

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = PaytmChecksum.verifySignature(response_dict, "AlulEP3fgbQClt4w", checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, '../templates/pages/paymentstatus.html', {'response': response_dict})
