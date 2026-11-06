"""
"""

import os

#from datetime import timedelta
#from django.utils import timezone
#from dracogate.models import VirtualMorph

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aenir_web.settings")

app = Celery("aenir_web")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# NOTE: django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
#@app.task
def clean_vmorphs():
    """
    Clean up owner-less vmorphs that are a day or more older every seven days.
    """
    #VirtualMorph.objects.filter(owner=None, creation_date__lt=timezone.now() - timedelta(days=1)).delete()
