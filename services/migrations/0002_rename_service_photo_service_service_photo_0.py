# Generated by Django 3.2.14 on 2023-04-14 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='service_photo',
            new_name='service_photo_0',
        ),
    ]
