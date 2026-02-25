"""
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from aenir.morph import Morph
from aenir import get_morph

User = get_user_model()

def validate_history(history):
    """
    """
    for method, kwargs in history:
        logger.info("%s(**%r)", method, kwargs)

class VirtualMorph(models.Model):
    """
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    # meta: composite pk
    morph_id = models.CharField(
        #min_length=1,
        max_length=25,
        # For forms only
        #blank=False,
        #null=False,
        #validators=[validate_morph_id],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    # initialization
    game_no = models.PositiveSmallIntegerField(
        #validators=[validate_game_no],
    )
    name = models.CharField(
        max_length=9,
        blank=False,
    )
    options = models.JSONField(
        #validators=[validate_options],
        default=dict,
        blank=True,
    )
    # post-initialization
    history = models.JSONField(
        default=list,
        #validators=[validate_history],
        blank=True,
    )

    class Meta:
        unique_together = [
            ["user", "morph_id"],
        ]

    def init(self) -> Morph:
        """
        """
        game_no = self.game_no
        name = self.name
        options = self.options
        morph = get_morph(game_no, name, **options)
        for method, kwargs in self.history:
            logger.info("%s(**%r)", method, kwargs)
            getattr(self, method)(**kwargs)
        self.morph = morph
        return morph

    def level_up(self, **kwargs):
        """
        Levels up a morph.
        """
        morph = self.morph
        num_levels = int(kwargs.get("num_levels"))
        try:
            morph.level_up(num_levels)
            param_bounds = None
            self.history.append(("level_up", {"num_levels": num_levels}))
        except LevelUpError as err:
            #value = morph.max_level
            param_bounds = err.max_level
            is_success = False
        return (morph, param_bounds)

    def promote(self, **kwargs):
        """
        Promotes a morph.
        """
        morph = self.morph
        promo_cls = kwargs.get("promo_cls")
        morph.promo_cls = promo_cls
        is_success: bool
        try:
            morph.promote()
            param_bounds = None
            self.history.append(("promote", {}))
        except PromotionError as err:
            param_bounds = err.promotion_list
        return (morph, param_bounds)

    # FE5,6,7,8,9
    def use_stat_booster(self, **kwargs):
        """
        Uses a stat booster on a morph.
        """
        morph = self.morph
        item_name = kwargs.get("item_name")
        try:
            morph.use_stat_booster(item_name)
            param_bounds = None
            self.history.append(("use_stat_booster", {"item_name": item_name}))
        except StatBoosterError as err:
            param_bounds = err.valid_stat_boosters
        return (morph, param_bounds)

    # FE5
    def equip_scroll(self, **kwargs):
        """
        Equips a growth-altering scroll onto on a morph. (FE5 only!)
        """
        morph = self.morph
        scroll_name = kwargs.get("scroll_name")
        try:
            morph.equip_scroll(scroll_name)
            param_bounds = None
            self.history.append(("equip_scroll", {"scroll_name": scroll_name}))
        except StatBoosterError as err:
            param_bounds = err.valid_scrolls
        return (morph, param_bounds)

    def unequip_scroll(self, **kwargs):
        """
        Unequips a growth-altering scroll from a morph. (FE5 only!)
        """
        morph = self.morph
        scroll_name = kwargs.get("scroll_name")
        try:
            morph.unequip_scroll(scroll_name)
            param_bounds = None
            self.history.append(("unequip_scroll", {"scroll_name": scroll_name}))
        except StatBoosterError as err:
            param_bounds = err.valid_scrolls
        return (morph, param_bounds)

    # FE7
    def use_afas_drops(self, **kwargs):
        """
        Uses Afa's Drops on a morph. (FE7 only!)
        """
        morph = self.morph
        try:
            morph.use_afas_drops()
            param_bounds = None
            self.history.append(("use_afas_drops", {}))
        except GrowthsItemError as err:
            param_bounds = err.reason
        return (morph, param_bounds)

    # FE8
    def use_metiss_tome(self, **kwargs):
        """
        Uses Metis' Tome on a morph. (FE8 only!)
        """
        morph = self.morph
        try:
            morph.use_metiss_drops()
            param_bounds = None
            self.history.append(("use_afas_drops", {}))
        except GrowthsItemError as err:
            param_bounds = err.reason
        return (morph, param_bounds)

    # FE8
    def equip_knight_ward(self, **kwargs):
        """
        Equips the Knight Ward on a morph. (FE9 Knights only!)
        """
        morph = self.morph
        try:
            morph.equip_knight_ward()
            param_bounds = None
            self.history.append(("equip_knight_ward", {}))
        except GrowthsItemError as err:
            param_bounds = err.reason
        return (morph, param_bounds)

    # FE8
    def unequip_knight_ward(self, **kwargs):
        """
        Unequips the Knight Ward from a morph. (FE9 Knights only!)
        """
        morph = self.morph
        try:
            morph.equip_knight_ward()
            param_bounds = None
            self.history.append(("unequip_knight_ward", {}))
        except GrowthsItemError as err:
            param_bounds = err.reason
        return (morph, param_bounds)

    # FE9
    def equip_band(self, **kwargs):
        """
        Equips a growth-altering band onto on a morph. (FE9 only!)
        """
        morph = self.morph
        band_name = kwargs.get("band_name")
        try:
            morph.equip_band(band_name)
            param_bounds = None
            self.history.append(("equip_band", {"band_name": band_name}))
        except BandError as err:
            param_bounds = err.valid_bands
        return (morph, param_bounds)

    def unequip_band(self, **kwargs):
        """
        Unequips a growth-altering band from a morph. (FE9 only!)
        """
        morph = self.morph
        band_name = kwargs.get("band_name")
        try:
            morph.unequip_band(band_name)
            param_bounds = None
            self.history.append(("unequip_band", {"band_name": band_name}))
        except BandError as err:
            param_bounds = err.valid_bands
        return (morph, param_bounds)

