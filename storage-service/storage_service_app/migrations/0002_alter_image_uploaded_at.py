# Generated by Django 4.1 on 2024-07-03 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_service_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uploaded_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 3, 12, 49, 46, 263682)),
        ),
    ]
