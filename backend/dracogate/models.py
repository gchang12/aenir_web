"""
"""

#from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

def vmorph_name_generator():
    """
    """
    now = timezone.now()
    return now.isoformat()

class VirtualMorph(models.Model):
    """
    """
    # meta
    owner = models.ForeignKey(
        to=User,
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        default=vmorph_name_generator,
        max_length=32,
    )
    # init
    game_no = models.PositiveSmallIntegerField(
        #min_value=4,
        #max_value=9,
    )
    unit = models.CharField(
        #max_length=9,
    )
    init_options = models.JSONField(
        default=dict,
    )
    # display
    history = models.JSONField(
        default=list,
    )
    stats = models.JSONField(
        default=dict,
    )

    class Meta:
        unique_together = ["owner", "name"]
