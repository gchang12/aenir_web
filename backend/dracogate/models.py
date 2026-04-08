"""
"""

import uuid
from datetime import datetime 
from dataclasses import dataclass
from typing import NamedTuple

from django.db import models
from django.contrib.auth import get_user_model

from aenir import get_morph

User = get_user_model()

class Stat(NamedTuple):
    """
    """
    id: str
    current_val: float
    growth_rate: int | None
    max_val: float
    absmax_val: float

class VirtualMorph(models.Model):
    """
    """
    # meta
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
    modification_date = models.DateField(
        auto_now=True,
    )
    morph_id = models.CharField(
        max_length=25,
    )
    # initialization
    game_no = models.PositiveSmallIntegerField()
    name = models.CharField(
        max_length=9,
    )
    options = models.JSONField(
        default=dict,
        blank=True,
    )
    # progression
    history = models.JSONField(
        default=list,
        blank=True,
    )
    # to show on-screen as a preview
    progress = models.JSONField()

    class Meta:
        """
        """
        unique_together = [
            ["owner", "morph_id"],
        ]

    @staticmethod
    def _generate_morph_id(game_no, name):
        """
        """
        now = datetime.now()
        date_name = now.isoformat()
        trimmed_date_name = date_name[:date_name.index('.')][5:].replace('T', '_').replace('-', '').replace(':', '')
        morph_id = "FE%d!%s-%s" % (game_no, name, trimmed_date_name)
        return morph_id

    def save(self, **kwargs):
        """
        """
        try:
            morph = self.morph
        except AttributeError:
            morph = get_morph(self.game_no, self.name, **self.options)
        self.progress = {
            "current_cls": morph.current_cls,
            "current_lv": morph.current_lv,
        }
        #self.morph_id = self.generate_morph_id()
        #print("save", self.morph_id)
        return super().save(**kwargs)

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

    def _generate_stats(self):
        """
        """
        morph = self.morph
        current_stats = morph.current_stats.as_dict()
        growth_rates = morph.growth_rates.as_dict()
        max_stats = morph.max_stats.as_dict()
        absmax_stats = morph.Stats.ABSOLUTE_MAXES()
        # nullify zero-growth stats
        zero_growth_stat_list = morph.Stats.ZERO_GROWTH_STAT_LIST()
        for indexno, statname in enumerate(morph.Stats.STAT_LIST()):
            yield Stat(
                id=statname,
                current_val=current_stats[statname] / 100,
                growth_rate=(None if statname in zero_growth_stat_list else growth_rates[statname]),
                max_val=max_stats[statname] / 100,
                absmax_val=absmax_stats[indexno] / 100,
            )

