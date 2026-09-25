"""
"""

#from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from aenir import (
    get_morph,
    get_morph_class,
    LevelUpError,
    PromotionError,
    StatBoosterError,
    GrowthsItemError,
    ScrollError,
    BandError,
    KnightWardError,
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

    @staticmethod
    def action_forecast_bases(morph, delta_dict):
        """
        """
        absmax_stats = morph.Stats.ABSOLUTE_MAXES()
        for indexno, stat in enumerate(morph.Stats.STAT_LIST()):
            base = getattr(morph.current_stats, stat)
            max_ = getattr(morph.max_stats, stat)
            absmax = absmax_stats[indexno]
            if delta_dict is not None:
                delta = (None if delta_dict[stat] is None else delta_dict[stat] / 100)
            else:
                delta = None
            yield {
                "name": stat,
                "value": base / 100,
                "max": max_ / 100,
                "absmax": absmax / 100,
                "delta": delta,
            }

    @staticmethod
    def action_forecast_growths(morph, delta_dict):
        """
        """
        for indexno, stat in enumerate(morph.Stats.STAT_LIST()):
            growth = getattr(morph.growth_rates, stat)
            max_ = getattr(morph.max_stats, stat)
            if delta_dict is not None:
                delta = (None if delta_dict[stat] is None else delta_dict[stat] / 100)
            else:
                delta = None
            yield {
                "name": stat,
                "value": growth,
                "max": 100,
                "absmax": 100,
                "delta": delta,
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
        morph_class = get_morph_class(self.game_no)
        morph = morph_class.from_dict(self.stats)
        #morph = get_morph(self.game_no, self.unit, **self.init_options)
        #for action, params in self.history: getattr(morph, action)(**params)
        #print(morph._miscellany)
        self.morph = morph
        return morph

    def save(self, **kwds):
        """
        """
        try:
            self.stats = self.morph.as_dict()
        except AttributeError as e:
            self.morph = get_morph(self.game_no, self.unit, **self.init_options)
            self.stats = self.morph.as_dict()
        return super().save(**kwds)

    def level_up(self, num_levels: int):
        """
        """
        is_success: bool
        try:
            self.morph.level_up(num_levels)
            param_bounds = {}
            self.history.append(
                ("level_up", {"num_levels": num_levels})
            )
            is_success = True
        except LevelUpError as e:
            min_lv, max_lv = e.level_range
            param_bounds = {
                "min_lv": min_lv,
                "max_lv": max_lv,
            }
            is_success = False
        return (is_success, param_bounds)

    def promote(self, promo_cls: str):
        """
        """
        is_success: bool
        try:
            self.morph.promote(promo_cls=promo_cls)
            self.history.append(
                ("promote", {'promo_cls': self.morph.current_cls})
            )
            param_bounds = {}
            is_success = True
            #print(self.history)
        except PromotionError as e:
            param_bounds = {
                e.Reason.NO_PROMOTIONS: None,
                e.Reason.LEVEL_TOO_LOW: {"min_promo_level": e.min_promo_level, "promotions": e.promotion_list},
                e.Reason.INVALID_PROMOTION: {"promotions": e.promotion_list},
            }[e.reason]
            is_success = False
            #print(e.reason)
        #print(is_success)
        return (is_success, param_bounds)

    def use_stat_booster(self, item_name: str):
        """
        """
        is_success: bool
        try:
            #print(self.morph._miscellany)
            self.morph.use_stat_booster(item_name)
            self.history.append(
                ("use_stat_booster", {"item_name": item_name}),
            )
            param_bounds = {}
            is_success = True
        except StatBoosterError as e:
            param_bounds = {
                StatBoosterError.Reason.NOT_FOUND: {"stat_boosters": e.valid_stat_boosters},
                StatBoosterError.Reason.STAT_IS_MAXED: None,
            }[e.reason]
            is_success = False
        except NotImplementedError as e:
            raise e
        return (is_success, param_bounds)

    def use_afas_drops(self, to_consume: bool):
        """
        """
        is_success: bool
        if to_consume is True:
            try:
                self.morph.use_afas_drops()
                self.history.append(
                    ("use_afas_drops", {}),
                )
                is_success = True
                param_bounds = {}
            except GrowthsItemError as e:
                is_success = False
                param_bounds = None
        else:
            is_success = False
            param_bounds = {}
        return (is_success, param_bounds)

    def set_scrolls(self, scrolls: list[str]):
        """
        """
        is_success: bool
        try:
            self.morph.set_scrolls(scrolls)
            self.history.append(
                ("set_scrolls", {"scrolls": scrolls}),
            )
            param_bounds = {}
            is_success = True
        except ScrollError as e:
            param_bounds = {
                ScrollError.Reason.NOT_FOUND: {"scrolls": tuple(self.morph.scroll_dict)},
                ScrollError.Reason.NO_INVENTORY_SPACE: {"inventory_size": self.morph.inventory_size},
            }[e.reason]
            is_success = False
        return (is_success, param_bounds)

    def shapeshift(self, to_shapeshift: bool):
        """
        """
        is_success: bool
        if self.morph.is_laguz is False:
            is_success = False
            param_bounds = None
        else:
            if to_shapeshift is False:
                param_bounds = {"cls_to_transform_to": self.morph._miscellany["cls_to_transform_to"]}
                is_success = False
            else:
                method_name = {
                    True: "revert",
                    False: "transform",
                }[self.morph._miscellany["is_transformed"]]
                getattr(self.morph, method_name)()
                self.history.append(
                    (method_name, {}),
                )
                param_bounds = None
                is_success = True
        return (is_success, param_bounds)

    def set_demiband(self, to_shapeshift: bool):
        """
        """
        is_success: bool
        if self.morph.is_laguz is False:
            is_success = False
            param_bounds = None
        else:
            if to_shapeshift is False:
                param_bounds = {"cls_to_transform_to": self.morph._miscellany["cls_to_transform_to"]}
                is_success = False
            else:
                method_name = {
                    True: "unequip_demi_band",
                    False: "equip_demi_band",
                }[self.morph._miscellany["is_transformed"]]
                try:
                    getattr(self.morph, method_name)()
                    self.history.append(
                        (method_name, {}),
                    )
                    param_bounds = {}
                    is_success = True
                except DemiBandError as e:
                    if e.reason == DemiBandError.Reason.NO_INVENTORY_SPACE:
                        param_bounds = None
                        is_success = False
        return (is_success, param_bounds)

    def set_bands(self, bands: list[str]):
        """
        """
        is_success: bool
        #demi_band_was_on = False
        if "Demi Band" in self.morph._miscellany["equipped_bands"]:
            self.morph.unequip_demi_band()
            if "Demi Band" not in bands:
                bands.append("Demi Band")
        if "Knight Ward" in self.morph._miscellany["equipped_bands"]:
            self.morph.unequip_knight_ward()
            if "Knight Ward" not in bands:
                bands.append("Knight Ward")
        try:
            self.morph.set_bands(bands)
            self.history.append(
                ("set_bands", {"bands": bands}),
            )
            param_bounds = {}
            is_success = True
        except (KnightWardError, BandError) as e:
            param_bounds = {
                BandError.Reason.NOT_FOUND: {"bands": tuple(self.morph.band_dict)},
                BandError.Reason.NO_INVENTORY_SPACE: {"inventory_size": self.morph.inventory_size},
                KnightWardError.Reason.NOT_A_KNIGHT: None,
            }[e.reason]
            is_success = False
        return (is_success, param_bounds)

    def use_metiss_tome(self, to_consume: bool):
        """
        """
        is_success: bool
        if to_consume is True:
            try:
                self.morph.use_metiss_tome()
                self.history.append(
                    ("use_metiss_tome", {}),
                )
                is_success = True
                param_bounds = {}
            except GrowthsItemError as e:
                is_success = False
                param_bounds = None
        else:
            is_success = False
            param_bounds = {}
        return (is_success, param_bounds)

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

