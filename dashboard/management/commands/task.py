from django.core.management.base import BaseCommand
import schedule
import time
from dashboard.models import TestTaskOnHeroku
import datetime

class Command(BaseCommand):
    help = 'Run a scheduled task'

    def handle(self, *args, **options):
        # Define your task function
        tm =  datetime.datetime.now()
        TestTaskOnHeroku.objects.create(data=f"Created {tm}")
        return  'created'
