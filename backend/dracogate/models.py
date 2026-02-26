"""
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from aenir import get_morph
from aenir._exceptions import (
    UnitNotFoundError,
    LevelUpError,
    PromotionError,
    StatBoosterError,
    ScrollError,
    BandError,
    GrowthsItemError,
    KnightWardError,
    InitError,
)
from aenir_web._logging import logger

User = get_user_model()

class VirtualMorph(models.Model):
    """
    """
    id = models.AutoField(
        primary_key=True,
    )
    # meta: composite pk
    morph_id = models.CharField(
        max_length=25,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    # initialization
    game_no = models.PositiveSmallIntegerField()
    name = models.CharField(
        max_length=9,
        blank=False,
    )
    options = models.JSONField(
        default=dict,
        blank=True,
    )
    # post-initialization
    history = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta:
        unique_together = [
            ["user", "morph_id"],
        ]

    def init(self):
        """
        """
        game_no = self.game_no
        name = self.name
        options = self.options
        logger.debug("Now calling get_morph(%d, '%s', **%r)", game_no, name, options)
        morph = get_morph(game_no, name, **options)
        for method, kwargs in self.history:
            logger.info("%s(**%r)", method, kwargs)
            getattr(morph, method)(**kwargs)
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
            param_bounds = {
                LevelUpError.Reason.NOT_POSITIVE: err.level_range,
                LevelUpError.Reason.EXCEEDS_MAX: err.level_range[1],
            }[err.reason]
        return param_bounds

    def promote(self, **kwargs):
        """
        Promotes a morph.
        """
        morph = self.morph
        promo_cls = kwargs.get("promo_cls")
        morph.promo_cls = promo_cls
        morph._set_min_promo_level()
        min_promo_level = morph.min_promo_level
        try:
            morph.promote()
            param_bounds = ([morph.current_cls], min_promo_level)
            self.history.append(("promote", {"promo_cls": promo_cls}))
        except PromotionError as err:
            param_bounds = {
                err.Reason.NO_PROMOTIONS: ([], 0),
                err.Reason.LEVEL_TOO_LOW: (None, min_promo_level),
                err.Reason.INVALID_PROMOTION: (err.promotion_list, 0),
            }[err.reason]
        return param_bounds

    # FE5,6,7,8,9
    def use_stat_booster(self, **kwargs):
        """
        Uses a stat booster on a morph.
        """
        morph = self.morph
        item_name = kwargs.get("item_name")
        logger.debug("item_name: %r", item_name)
        try:
            morph.use_stat_booster(item_name)
            param_bounds = None
            self.history.append(("use_stat_booster", {"item_name": item_name}))
        except StatBoosterError as err:
            param_bounds = {
                err.Reason.NOT_FOUND: err.valid_stat_boosters,
                err.Reason.STAT_IS_MAXED: err.max_stat,
            }[err.reason]
        return param_bounds

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
        except ScrollError as err:
            param_bounds = {
                err.Reason.NOT_FOUND: err.valid_scrolls,
                # TODO: Return list of items that can be tossed.
                err.Reason.NO_INVENTORY_SPACE: err.valid_scrolls,
                #err.Reason.NOT_EQUIPPED: err.valid_scrolls,
                err.Reason.ALREADY_EQUIPPED: err.valid_scrolls,
            }[err.reason]
        return param_bounds

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
        except ScrollError as err:
            param_bounds = {
                err.Reason.NOT_FOUND: err.valid_scrolls,
                # TODO: Return list of items that can be tossed.
                err.Reason.NO_INVENTORY_SPACE: err.valid_scrolls,
                err.Reason.NOT_EQUIPPED: err.valid_scrolls,
                #err.Reason.ALREADY_EQUIPPED: err.valid_scrolls,
            }[err.reason]
        return param_bounds

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
            param_bounds = {
                err.Reason.ALREADY_CONSUMED: err.consumption_date,
            }[err.reason]
        return param_bounds

    # FE8
    def use_metiss_tome(self, **kwargs):
        """
        Uses Metis' Tome on a morph. (FE8 only!)
        """
        morph = self.morph
        try:
            morph.use_metiss_tome()
            param_bounds = None
            self.history.append(("use_metiss_tome", {}))
        except GrowthsItemError as err:
            param_bounds = {
                err.Reason.ALREADY_CONSUMED: err.consumption_date,
            }[err.reason]
        return param_bounds

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
        except KnightWardError as err:
            param_bounds = {
                err.Reason.NOT_A_KNIGHT: err.knights,
                err.Reason.ALREADY_EQUIPPED: err.valid_bands,
                #err.Reason.NOT_EQUIPPED: None,
                # TODO: Return list of items that can be tossed.
                err.Reason.NO_INVENTORY_SPACE: err.valid_bands,
            }[err.reason]
        return param_bounds

    # FE8
    def unequip_knight_ward(self, **kwargs):
        """
        Unequips the Knight Ward from a morph. (FE9 Knights only!)
        """
        morph = self.morph
        try:
            morph.unequip_knight_ward()
            param_bounds = None
            self.history.append(("unequip_knight_ward", {}))
        except KnightWardError as err:
            param_bounds = {
                err.Reason.NOT_A_KNIGHT: err.knights,
                #err.Reason.ALREADY_EQUIPPED: None,
                err.Reason.NOT_EQUIPPED: err.reason,
                #err.Reason.NO_INVENTORY_SPACE: morph.equipped_bands,
            }[err.reason]
        return param_bounds

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
            param_bounds = {
                err.Reason.NOT_FOUND: err.valid_bands,
                # TODO: Return list of items that can be tossed.
                err.Reason.NO_INVENTORY_SPACE: err.valid_bands,
                err.Reason.ALREADY_EQUIPPED: err.valid_bands,
            }[err.reason]
        return param_bounds

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
            param_bounds = {
                err.Reason.NOT_FOUND: err.valid_bands,
                # TODO: Return list of items that can be tossed.
                err.Reason.NO_INVENTORY_SPACE: err.valid_bands,
                err.Reason.NOT_EQUIPPED: err.valid_bands,
                #err.Reason.ALREADY_EQUIPPED: err.valid_bands,
            }[err.reason]
        return param_bounds

