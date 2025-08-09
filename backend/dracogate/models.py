"""
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Morph(models.Model):
    """
    """
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    game = models.PositiveSmallIntegerField()
    unit_name = models.CharField()
    unit_stats = models.JSONField()
    miscellany = models.JSONField()
