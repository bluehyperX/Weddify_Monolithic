from django.db import models
from datetime import datetime

# Create your models here.
class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    event_date = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=50, blank=True)
    service_id = models.IntegerField(default=1)
    vendor_id = models.IntegerField(default=1)
    user_id = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.first_name