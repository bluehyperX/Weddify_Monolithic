from django.urls import path
from orders import views

urlpatterns = [
    path('payment', views.payment, name='payment'),
    path('<int:id>', views.delete_order, name='delete_order'),
]