from django.db import models
from datetime import datetime
from .storage import MinioStorage

class Image(models.Model):
    image = models.ImageField(upload_to='', storage=MinioStorage())
    minio_url = models.URLField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.minio_url = self.image.url
            self.save(update_fields=['minio_url'])

    def __str__(self):
        return self.image.name

    class Meta:
        db_table = 'Images'