import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClerkFoodhub.settings')

app = Celery('ClerkFoodhub')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'week_task': {
        'task': 'catering.tasks.week_update_catering',
        'schedule': crontab(minute=1, hour=[5, 12, 17], day_of_week=1),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
