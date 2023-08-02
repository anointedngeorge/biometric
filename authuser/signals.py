from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from authuser.models import StudentModel


@receiver(post_save, sender='authuser.StudentModel')
def post_save_create_student(sender, instance, created, *args, **kwargs):
    if created:
        filename = str(instance.picture_url).split('/')[1].split('.')[0] if instance.picture_url  else ''
        instance.picture_name = filename
        instance.save()
