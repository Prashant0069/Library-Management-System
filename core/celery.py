import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Use a string here means the worker doesn't have to serialize 
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery Beat Schedule
app.conf.beat_schedule = {
    'generate-daily-report': {
        'task': 'reports.tasks.generate_library_report',
        # 'schedule': 86400.0,  # Daily (24 hours)
        'schedule': 60.0,  # Daily (1 minute)
    },
}
