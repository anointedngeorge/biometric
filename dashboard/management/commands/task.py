from django.core.management.base import BaseCommand
import schedule
import time
from dashboard.models import *

import datetime



class Command(BaseCommand):
    help = 'Run a scheduled task'

    def handle(self, *args, **options):
        # Define your task function
        tm =  datetime.datetime.now()
        CreateAttendance.objects.all().update(status='finished')
        # TestTaskOnHeroku.objects.create(data=f"Created {tm}")
        return  'created'

