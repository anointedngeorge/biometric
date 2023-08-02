from django.db import models
import uuid
from django.utils import timezone

class CoreDb(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateField(auto_created=True, default=timezone.now, editable=False)

    class Meta:
        abstract=True