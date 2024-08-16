# models.py
from django.db import models
from datetime import datetime


class Image(models.Model):
    image = models.ImageField(upload_to='media/')
    uploaded_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.image.name

    class Meta:
        db_table = 'Images'
