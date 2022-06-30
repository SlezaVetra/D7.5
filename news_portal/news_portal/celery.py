import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')

app = Celery('news_portal')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.timezone = "Europe/Moscow"
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'post.tasks.send_weekly_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=7),
    },
}
app.autodiscover_tasks()
