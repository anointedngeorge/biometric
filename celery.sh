# celery -A periodictask worker -l info
# celery -A periodictask beat -l info 

celery -A periodictask worker --beat --scheduler django --loglevel=info

# celery -A periodictask beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler