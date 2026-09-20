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

class StatsBundler:
    """
    """

    @staticmethod
    def init_forecast(morph):
        """
        """
        # iterable of (base, growth, max, absmax)
        absmax_stats = morph.Stats.ABSOLUTE_MAXES()
        zerogrowth_stats = morph.Stats.ZERO_GROWTH_STAT_LIST()
        for indexno, stat in enumerate(morph.Stats.STAT_LIST()):
            base = getattr(morph.current_stats, stat)
            growth = getattr(morph.growth_rates, stat)
            max_ = getattr(morph.max_stats, stat)
            absmax = absmax_stats[indexno]
            yield {
                "name": stat,
                "base": base / 100,
                "growth": (growth if stat not in zerogrowth_stats else None),
                "max": max_ / 100,
                "absmax": absmax / 100,
            }

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

