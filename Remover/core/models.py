from django.db import models

class ImageUpload(models.Model):
    upload_count = models.IntegerField(default=0)
