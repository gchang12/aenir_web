"""
"""

#from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from aenir import (
    get_morph_class,
    LevelUpError,
)

User = get_user_model()

def vmorph_name_generator():
    """
    """
    now = timezone.now()
    now_isoformat = now.isoformat()
    return now_isoformat[:now_isoformat.index(".")]

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
    creation_date = models.DateTimeField(
        auto_now_add=True,
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
        """
        """
        unique_together = ["owner", "name"]

    def init(self):
        """
        """
        data = {}
        data['game'] = self.game_no
        data['name'] = self.unit
        data['init_options'] = self.init_options
        data['_miscellany'] = {}
        data.update(self.stats)
        morph_class = get_morph_class(self.game_no)
        morph = morph_class.from_dict(data)
        self.morph = morph
        return morph

    def level_up(self, num_levels: int):
        """
        """
        try:
            self.morph.level_up(num_levels)
            param_bounds = {}
        except LevelUpError as e:
            min_lv, max_lv = e.level_range
            param_bounds = {
                "min_lv": min_lv,
                "max_lv": max_lv,
            }
        return param_bounds

'''
    def path_to(cls, file: str) -> str:
    def query_db(
    def lookup(
    def as_dict(self):
    def from_dict(cls, data):
    def game(self) -> FireEmblemGame:
    def name(self) -> str | None:
    def init_options(self) -> dict:
    def get_growths_augment(self):
    def get_promotion_list(self) -> List[str]:
    def copy(self) -> Self:
    def get_promotion_item(self) -> str | None:
    def inventory_size(self) -> int:
    def inventory_size(self) -> int:
    def game(self) -> FireEmblemGame:
    def name(self) -> str | None:
    def father(self) -> str | None:
    def get_promotion_item(self) -> str | None:
    def inventory_size(self) -> int:
    def get_promotion_item(self) -> str | None:
    def inventory_size(self) -> int:
    def get_promotion_item(self) -> str | None:
    def inventory_size(self) -> int:
    def inventory_size(self) -> int:
    def get_promotion_item(self) -> str | None:
    def inventory_size(self) -> int:
    def get_promotion_item(self) -> str | None:
    def roundup_stats(dictlike: dict[str, int]):
'''

'''
    def level_up(self, num_levels: int) -> None:
    def promote(self, *, promo_cls=None) -> None:
    def use_stat_booster(self, item_name: str) -> None:
    def use_stat_booster(self, item_name: str) -> None:
    def promote(self, *, promo_cls=None) -> None:
    def promote(self, *, promo_cls=None) -> None:
    def set_scrolls(self, scrolls):
    def unequip_scroll(self, scroll_name: str) -> None:
    def equip_scroll(self, scroll_name: str) -> None:
    def use_afas_drops(self) -> None:
    def promote(self, *, promo_cls=None) -> None:
    def use_metiss_tome(self) -> None:
    def equip_band(self, band_name: str) -> None:
    def unequip_band(self, band_name: str) -> None:
    def equip_knight_ward(self) -> None:
    def unequip_knight_ward(self) -> None:
    def set_knight_ward(self, equip: bool):
    def set_bands(self, bands):
    def transform(self):
    def revert(self):
    def equip_demi_band(self):
    def unequip_demi_band(self):
'''
