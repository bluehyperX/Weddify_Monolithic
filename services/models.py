from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.

class Service (models.Model):

    service_type_choice = (
        ('Photographer', 'Photographer'),
        ('Venue', 'Venue'),
        ('Caterer', 'Caterer'),
        ('Bridal Services', 'Bridal Services'),
    )

    state_choice = (
        ('Delhi', 'Delhi'),
        ('Maharastra', 'Maharastra'),
        ('Karnataka', 'Karnataka'),
        ('Telangana', 'Telangana'),
        ('West Bengal', 'West Bengal'),
        ('Haryana', 'Haryana'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Rajasthan', 'Rajasthan'),
    )

    title = models.CharField(max_length=255)
    service_type = models.CharField(choices=service_type_choice, max_length=100)
    vendor_id =models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(choices=state_choice, max_length=100)
    featured_package_price = models.IntegerField()
    service_photo = models.FileField(upload_to='photos/%y/%m/%d/')
    service_photo_1 = models.FileField(upload_to='photos/%y/%m/%d/', blank=True)
    service_photo_2 = models.FileField(upload_to='photos/%y/%m/%d/', blank=True)
    service_photo_3 = models.FileField(upload_to='photos/%y/%m/%d/', blank=True)
    service_photo_4 = models.FileField(upload_to='photos/%y/%m/%d/', blank=True)
    description = RichTextField()
    other_details = RichTextField()
    is_featured = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title