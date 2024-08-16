from django.db import models
from datetime import datetime
from django.conf import settings

class Image(models.Model):
    image = models.ImageField(upload_to='')
    minio_url = models.URLField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.image.name

    class Meta:
        db_table = 'Images'

    def get_public_url(self):
        if self.minio_url:
            return self.minio_url.replace('http://minio:9000', settings.PUBLIC_MINIO_URL)
        return ''