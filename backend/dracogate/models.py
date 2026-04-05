"""
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Stat:
    """
    """

    def __init__(self, *, id, current_val, growth_rate, max_val, absmax_val, css_class):
        """
        """
        self.id = id
        self.current_val = current_val
        self.growth_rate = growth_rate
        self.max_val = max_val
        self.absmax_val = absmax_val
        self.css_class = css_class

    def as_dict(self):
        """
        """
        return {
            "id": self.id,
            "current_val": self.current_val,
            "growth_rate": self.growth_rate,
            "max_val": self.max_val,
            "absmax_val": self.absmax_val,
            "css_class": self.css_class,
        }

class VirtualMorph(models.Model):
    """
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    creation_date = models.DateField(
        auto_now_add=True,
    )
    morph_id = models.CharField(
        max_length=25,
    )
    game_no = models.PositiveSmallIntegerField()
    name = models.CharField(
        max_length=9,
    )
    options = models.JSONField(
        default=dict,
        blank=True,
    )
    history = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta:
        """
        """
        unique_together = [
            ["owner", "morph_id"],
        ]

    def init(self):
        """
        """

    def level_up(self, num_levels):
        """
        """

    def use_stat_booster(self, item_name):
        """
        """

    def set_scrolls(self, scrolls):
        """
        """

    def use_afas_drops(self):
        """
        """

    def use_metiss_tome(self):
        """
        """

    def set_bands(self, bands):
        """
        """

    def transform(self):
        """
        """

    def revert(self):
        """
        """

    def equip_demi_band(self):
        """
        """

    def unequip_demi_band(self):
        """
        """

    def _generate_stats(self, css_class_dict=None):
        """
        """
        morph = self.morph
        current_stats = morph.current_stats.as_dict()
        growth_rates = morph.growth_rates.as_dict()
        max_stats = morph.max_stats.as_dict()
        absmax_stats = morph.Stats.ABSOLUTE_MAXES()
        # null zero-growth stats
        zero_growth_stat_list = morph.Stats.ZERO_GROWTH_STAT_LIST()
        for indexno, statname in enumerate(morph.Stats.STAT_LIST()):
            yield Stat(
                id=statname,
                current_val=current_stats[statname] / 100,
                growth_rate=(None if statname in zero_growth_stat_list else growth_rates[statname]),
                max_val=max_stats[statname] / 100,
                absmax_val=absmax_stats[indexno] / 100,
                css_class=(None if css_class_dict is None else css_class_dict[statname]),
            ).as_dict()
