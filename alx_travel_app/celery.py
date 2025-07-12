# alx_travel_app/celery.py

import os
from celery import Celery

# Ensure Django settings are used for the Celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# Create the Celery app instance with your project name
app = Celery('alx_travel_app')

# Load config from Django settings using the CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from your installed apps
app.autodiscover_tasks()