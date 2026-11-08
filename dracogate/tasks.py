"""
"""

from celery import Celery
from celery.schedules import crontab

from aenir_web.celery import app
from .models import VirtualMorph

@app.task
def clean_vmorphs():
    """
    Clean up owner-less vmorphs that are a day or more older every seven days.
    """
    VirtualMorph.objects.filter(owner=None, creation_date__lt=timezone.now() - timedelta(days=1)).delete()

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    """
    """
    sender.add_periodic_task(
        crontab(day_of_week=1),
        clean_vmorphs.s(),
    )

# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
