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
from dracogate._logging import logger

User = get_user_model()

class VirtualMorph(models.Model):
    """
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
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
    creation_date = models.DateField(
        auto_now_add=True,
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
        logger.debug("get_morph(%d, '%s', **%r)", game_no, name, options)
        morph = get_morph(game_no, name, **options)
        for method, kwargs in self.history:
            getattr(morph, method)(**kwargs)
        self.morph = morph
        return morph

    def level_up(self, **kwargs):
        """
        Levels up a morph.
        """
        morph = self.morph
        previous_lv = morph.current_lv
        num_levels = int(kwargs.get("num_levels"))
        is_success: bool
        try:
            morph.level_up(num_levels)
            param_bounds = (previous_lv + 1, morph.max_level)
            self.history.append(("level_up", {"num_levels": num_levels}))
            is_success = True
        except LevelUpError as err:
            param_bounds = {
                # Invalid range. Please select a valid level.
                LevelUpError.Reason.NOT_POSITIVE: err.level_range,
                # Level has been maxed out at: #1! Please select valid level.
                LevelUpError.Reason.EXCEEDS_MAX: err.level_range, # TODO: Change this back to (min, max) format
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    def promote(self, **kwargs):
        """
        Promotes a morph.
        """
        morph = self.morph
        promo_cls = kwargs.get("promo_cls")
        morph.promo_cls = promo_cls
        morph._set_min_promo_level()
        min_promo_level = morph.min_promo_level
        is_success: bool
        try:
            morph.promote(promo_cls=promo_cls)
            self.history.append(("promote", {"promo_cls": promo_cls}))
            param_bounds = [
                (min_promo_level, morph.current_cls),
            ]
            is_success = True
        except PromotionError as err:
            if morph.current_lv < morph.max_level:
                morph.level_up(morph.max_level - morph.current_lv)
            try:
                morph.promote(promo_cls=promo_cls)
                param_bounds = [
                    (min_promo_level, morph.current_cls),
                ]
            except PromotionError as err2:
                if err2.reason == PromotionError.Reason.NO_PROMOTIONS:
                    param_bounds = None
                elif err2.reason == PromotionError.Reason.INVALID_PROMOTION:
                    param_bounds = []
                    for promo_cls2 in err2.promotion_list:
                        morph.promo_cls = promo_cls2
                        morph._set_min_promo_level()
                        param_bounds.append((morph.min_promo_level, promo_cls2))
            is_success = False
        # param_bounds: [(minpromolv: int, promocls: str)] | None
        return (is_success, param_bounds)

    # FE5,6,7,8,9
    def use_stat_booster(self, **kwargs):
        """
        Uses a stat booster on a morph.
        """
        morph = self.morph
        item_name = kwargs.get("item_name")
        logger.debug("item_name: %r", item_name)
        is_success: bool
        try:
            try:
                morph.use_stat_booster(item_name)
            except NotImplementedError as err:
                raise err
            param_bounds = None
            self.history.append(("use_stat_booster", {"item_name": item_name}))
            is_success = True
        except StatBoosterError as err:
            param_bounds = {
                # (Pass in "" as argument to get stat-booster list)
                err.Reason.NOT_FOUND: err.valid_stat_boosters,
                # stat #1 is already maxed at #2!
                err.Reason.STAT_IS_MAXED: err.max_stat,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # FE5
    def equip_scroll(self, **kwargs):
        """
        Equips a growth-altering scroll onto on a morph. (FE5 only!)
        """
        morph = self.morph
        scroll_name = kwargs.get("scroll_name")
        is_success: bool
        try:
            try:
                morph.equip_scroll(scroll_name)
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("equip_scroll", {"scroll_name": scroll_name}))
            is_success = True
        except ScrollError as err:
            param_bounds = {
                # (Pass in "" as argument to get list of scrolls)
                err.Reason.NOT_FOUND: err.valid_scrolls,
                # No inventory space. Please deselect some scrolls.
                err.Reason.NO_INVENTORY_SPACE: err.valid_scrolls,
                #err.Reason.NOT_EQUIPPED: err.valid_scrolls,
                # (scroll_name) is already equipped!
                err.Reason.ALREADY_EQUIPPED: err.valid_scrolls,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    def unequip_scroll(self, **kwargs):
        """
        Unequips a growth-altering scroll from a morph. (FE5 only!)
        """
        morph = self.morph
        scroll_name = kwargs.get("scroll_name")
        is_success: bool
        try:
            try:
                morph.unequip_scroll(scroll_name)
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("unequip_scroll", {"scroll_name": scroll_name}))
            is_success = True
        except ScrollError as err:
            param_bounds = {
                # That scroll was not found! Here is a list of valid scrolls. (Or you know, just an easy means of getting the scroll list)
                err.Reason.NOT_FOUND: err.valid_scrolls,
                # No inventory space! Please unequip some scrolls.
                err.Reason.NO_INVENTORY_SPACE: err.valid_scrolls,
                # (scroll_name) is not equipped! List of scrolls that ARE equipped.
                err.Reason.NOT_EQUIPPED: err.valid_scrolls,
                #err.Reason.ALREADY_EQUIPPED: err.valid_scrolls,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # FE7
    def use_afas_drops(self, **kwargs):
        """
        Uses Afa's Drops on a morph. (FE7 only!)
        """
        morph = self.morph
        is_success: bool
        try:
            try:
                morph.use_afas_drops()
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("use_afas_drops", {}))
            is_success = True
        except GrowthsItemError as err:
            param_bounds = {
                # (unit) has already consumed the item when they were a Lv#1 #2.
                err.Reason.ALREADY_CONSUMED: err.consumption_date,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # FE8
    def use_metiss_tome(self, **kwargs):
        """
        Uses Metis' Tome on a morph. (FE8 only!)
        """
        morph = self.morph
        is_success: bool
        try:
            try:
                morph.use_metiss_tome()
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("use_metiss_tome", {}))
            is_success = True
        except GrowthsItemError as err:
            param_bounds = {
                # (unit) has already consumed the item when they were a Lv#1 #2.
                err.Reason.ALREADY_CONSUMED: err.consumption_date,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # FE8
    def equip_knight_ward(self, **kwargs):
        """
        Equips the Knight Ward on a morph. (FE9 Knights only!)
        """
        morph = self.morph
        is_success: bool
        try:
            try:
                morph.equip_knight_ward()
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("equip_knight_ward", {}))
            is_success = True
        except KnightWardError as err:
            param_bounds = {
                # (unit) is not a knight and cannot equip the Knight Ward. List of knights:
                err.Reason.NOT_A_KNIGHT: err.knights,
                # Cannot equip Knight Ward. List of gear that CAN be equipped:
                err.Reason.ALREADY_EQUIPPED: err.valid_bands,
                #err.Reason.NOT_EQUIPPED: None,
                # Inventory is full. Please unequip some items.
                err.Reason.NO_INVENTORY_SPACE: err.valid_bands,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # FE8
    def unequip_knight_ward(self, **kwargs):
        """
        Unequips the Knight Ward from a morph. (FE9 Knights only!)
        """
        morph = self.morph
        is_success: bool
        try:
            try:
                morph.unequip_knight_ward()
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("unequip_knight_ward", {}))
            is_success = True
        except KnightWardError as err:
            param_bounds = {
                # (unit) is not a knight and cannot equip the Knight Ward. List of knights:
                err.Reason.NOT_A_KNIGHT: err.knights,
                #err.Reason.ALREADY_EQUIPPED: None,
                # Cannot unequip Knight Ward. List of gear that CAN be unequipped:
                # TODO: Change this in aenir.
                err.Reason.NOT_EQUIPPED: {band_name: (band_name in morph.equipped_bands) for band_name in morph.band_dict},
                #err.Reason.NO_INVENTORY_SPACE: morph.equipped_bands,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # FE9
    def equip_band(self, **kwargs):
        """
        Equips a growth-altering band onto on a morph. (FE9 only!)
        """
        morph = self.morph
        band_name = kwargs.get("band_name")
        is_success: bool
        try:
            try:
                morph.equip_band(band_name)
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("equip_band", {"band_name": band_name}))
            is_success = True
        except BandError as err:
            param_bounds = {
                # (Pass in "" as argument to get list of bands)
                err.Reason.NOT_FOUND: err.valid_bands,
                # No inventory space. Please deselect some bands.
                err.Reason.NO_INVENTORY_SPACE: err.valid_bands,
                # (band_name) is already equipped!
                err.Reason.ALREADY_EQUIPPED: err.valid_bands,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    def unequip_band(self, **kwargs):
        """
        Unequips a growth-altering band from a morph. (FE9 only!)
        """
        morph = self.morph
        band_name = kwargs.get("band_name")
        is_success: bool
        try:
            try:
                morph.unequip_band(band_name)
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("unequip_band", {"band_name": band_name}))
            is_success = True
        except BandError as err:
            param_bounds = {
                # That band was not found! Here is a list of valid bands. (Or you know, just an easy means of getting the band list)
                err.Reason.NOT_FOUND: err.valid_bands,
                # No inventory space! Please unequip some bands.
                err.Reason.NO_INVENTORY_SPACE: err.valid_bands,
                # (band_name) is not equipped! List of bands that ARE equipped.
                err.Reason.NOT_EQUIPPED: err.valid_bands,
                #err.Reason.ALREADY_EQUIPPED: err.valid_bands,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # TODO: Test this!
    def set_bands(self, **kwargs):
        """
        """
        morph = self.morph
        bands = kwargs.get("bands")
        is_success: bool
        try:
            try:
                morph.set_bands(bands)
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("set_bands", {"bands": list(bands)}))
            is_success = True
        except BandError as err:
            param_bounds = {
                # That band was not found! Here is a list of valid bands. (Or you know, just an easy means of getting the band list)
                BandError.Reason.NOT_FOUND: None,
                # No inventory space! Please unequip some bands.
                BandError.Reason.NO_INVENTORY_SPACE: None,
                # (band_name) is not equipped! List of bands that ARE equipped.
                #BandError.Reason.NOT_EQUIPPED: err.valid_bands,
                #err.Reason.ALREADY_EQUIPPED: err.valid_bands,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

    # TODO: Test this!
    def set_scrolls(self, **kwargs):
        """
        """
        morph = self.morph
        scrolls = kwargs.get("scrolls")
        is_success: bool
        try:
            try:
                morph.set_scrolls(scrolls)
            except AttributeError as err:
                raise NotImplementedError
            param_bounds = None
            self.history.append(("set_scrolls", {"scrolls": list(scrolls)}))
            is_success = True
        except ScrollError as err:
            param_bounds = {
                # That band was not found! Here is a list of valid bands. (Or you know, just an easy means of getting the band list)
                ScrollError.Reason.NOT_FOUND: None,
                # No inventory space! Please unequip some bands.
                ScrollError.Reason.NO_INVENTORY_SPACE: None,
                # (band_name) is not equipped! List of bands that ARE equipped.
                #BandError.Reason.NOT_EQUIPPED: err.valid_bands,
                #err.Reason.ALREADY_EQUIPPED: err.valid_bands,
            }[err.reason]
            is_success = False
        return (is_success, param_bounds)

