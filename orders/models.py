from django.db import models
from datetime import datetime

# Create your models here.
class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)
    title = models.CharField(max_length=50, blank=True)
    service_id = models.IntegerField(default=1)
    vendor_id = models.IntegerField(default=1)
    user_id = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        app_label = 'orders'
        db_table = 'orders'

    def __str__(self):
        return self.first_name