from django.shortcuts import render
from services.models import Service
from accounts.models import Vendor
# Create your views here.

def handler404(request, exception=None):
    return render(request, 'includes/404.html')

def home(request):
    featured_services = Service.objects.order_by('-created_date').filter(is_featured=True)
    all_services = Service.objects.order_by('-created_date').filter(is_featured=True)
    city_search = Service.objects.values_list('city', flat=True).distinct()
    state_search = Service.objects.values_list('state', flat=True).distinct()
    service_search = Vendor.objects.values_list('service_type', flat=True).distinct()
    data = {
        'featured_services' : featured_services,
        'city_search' : city_search,
        'state_search' : state_search,
        'service_search' : service_search,
        'all_services' : all_services,
    }
    return render(request, 'pages/home.html', data)

def search(request):
    services = Service.objects.order_by('-created_date').filter(is_featured=True)
    city_search = Service.objects.values_list('city', flat=True).distinct()
    state_search = Service.objects.values_list('state', flat=True).distinct()
    service_search = Service.objects.values_list('service_type', flat=True).distinct()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            services = services.filter(description__icontains=keyword)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            services = services.filter(city__iexact=city)

    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            services = services.filter(state__iexact=state)
    
    if 'service_type' in request.GET:
        service_type = request.GET['service_type']
        if service_type:
            services = services.filter(service_type__iexact=service_type)

    if 'min_featured_package_price' in request.GET:
        min_featured_package_price = request.GET['min_featured_package_price']
        max_featured_package_price = request.GET['max_featured_package_price']
        if max_featured_package_price:
           services = services.filter(featured_package_price__gte=min_featured_package_price, featured_package_price__lte=max_featured_package_price)
    data = {
        'services' : services,
        'city_search' : city_search,
        'state_search' : state_search,
        'service_search' : service_search,
    }
    return render(request, 'pages/search.html', data)