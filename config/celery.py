from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import configurations

# Set default Django settings module and configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

# Initialize Django configurations
configurations.setup()

# Create Celery app instance
app = Celery('tracker')

# Configure Celery with Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from Django apps
app.autodiscover_tasks()

# Configure the Celery Beat scheduler
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# Define periodic tasks
app.conf.beat_schedule = {
    'fetch-stock-prices-every-2-minutes': {
        'task': 'apps.tracking.tasks.fetch_and_broadcast_stock_prices',
        'schedule': crontab(minute='*/2'),  # Every 2 minutes
    },
}

# Set timezone
app.conf.timezone = 'Asia/Baku'  # You can use 'Asia/Baku' if you prefer Azerbaijan timezone
