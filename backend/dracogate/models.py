"""
"""

import uuid
from datetime import datetime 
from dataclasses import dataclass
from typing import NamedTuple

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from aenir import get_morph

User = get_user_model()

def validate_progress_value(progress_value):
    """
    """
    if not isinstance(progress_value, dict):
        raise ValidationError(
            _("Received object of type %(type)r"),
            params={"type": type(progress_value)},
        )
    if set(progress_value) != {"current_cls", "current_lv"}:
        raise ValidationError(
            _("Wrong keys in `progress_value`: %(keys)r"),
            params={"keys": progress_value.keys()},
        )
    if (type(progress_value["current_cls"]), type(progress_value["current_lv"])) != (str, int):
        raise ValidationError(
            _("Wrong value types in `progress_value`: %(values)r"),
            params={"value_types": {key: type(value) for key, value in progress_value.items()}},
        )


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
    progress = models.JSONField(
        validators=[validate_progress_value],
    )

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
            self.progress = {
                "current_cls": morph.current_cls,
                "current_lv": morph.current_lv,
            }
        except AttributeError:
            pass
        #self.morph_id = self.generate_morph_id()
        #print("save", self.morph_id)
        return super().save(**kwargs)

    def init(self):
        """
        """
        morph = get_morph(self.game_no, self.name, **self.options)
        for method_name, method_kwargs in self.history.items():
            getattr(morph, method_name)(**method_kwargs)
        self.morph = morph

    def level_up(self, num_levels):
        """
        """
        self.morph._set_max_level()
        is_success: bool
        try:
            self.morph.level_up(num_levels=num_levels)
            is_success = True
            param_bounds = (self.morph.current_lv + 1, self.morph.max_level)
        except LevelUpError as err:
            is_success = False
            # TODO: Check error type and return param-bounds based on that.
            param_bounds = err.param_bounds
        return (is_success, param_bounds)

    def promote(self, promo_cls):
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

