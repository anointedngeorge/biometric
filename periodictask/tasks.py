from celery import shared_task
from datetime import timedelta
import calendar


@shared_task
def runtask():
    print('Updated tasks')
    return 'Loading, i am coming to test...'




@shared_task
def check_time_interval():
    print('Checking time interval tasks')
    return 0