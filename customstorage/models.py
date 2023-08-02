from django.db import models
from customstorage.storage import CustomStorage

# Create your models here.

class FileStorageDb(models.Model):
    file_field_name = models.FileField(storage=CustomStorage())






