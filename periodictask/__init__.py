from .celery import app as celery_app
from periodictask.tasks import *



__all__ = ('celery_app',)

# # register this task
# runtask.delay()
