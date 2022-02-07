import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innowise_tech_sup.settings')
app = Celery('innowise_tech_sup')
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


