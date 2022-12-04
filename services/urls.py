from django.urls import path
from . import views
urlpatterns = [
     path('services', views.services, name='services'),
     path('add_service', views.add_service, name='add_service'),
     path('<int:id>', views.service_detail, name='service_detail'),
]