# your_app_name/tasks.py
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5  # Run every 5 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dsdf33434344'    # A unique code

    def do(self):
        # Your task logic goes here
        print('Yes, running it from a periodic cron tab...')
