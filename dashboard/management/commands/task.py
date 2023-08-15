from django.core.management.base import BaseCommand
import schedule
import time

class Command(BaseCommand):
    help = 'Run a scheduled task'

    def handle(self, *args, **options):
        # Define your task function
        return  "Hy loading"
