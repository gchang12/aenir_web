"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError, UnitNotFoundError

from dracogate._logging import logger

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """
    morphs = {}

    def create(self, request):
        """
        Creates a Morph instance and stores it in the 'morphs' attribute.
        """
        if len(self.morphs) == 5:
            raise Exception("Max capacity has been exceeded.")
        morph_id = request.data.get("morph_id")
        if not morph_id:
            raise Exception("'morph_id' was blank. Please try again.")
        if morph_id in self.morphs:
            raise Exception("The morph '%s' already exists." % morph_id)
        game_no, name, kwargs = self.parse_init_args(request.data)
        morph = get_morph(game_no, name, **kwargs)
        morph._set_max_level()
        self.morphs[morph_id] = morph
        # name, current, max, absMax
        statdicts = self.serialize_current_stats(morph)
        data = self.serialize_morph(morph, *statdicts)
        return Response({"id": morph_id, "morph": data})

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        game_no, name, kwargs = self.parse_init_args(request.query_params)
        try:
            morph = get_morph(game_no, name, **kwargs)
            morph._set_max_level()
            # name, current, max, absMax
            statdicts = self.serialize_current_stats(morph)
            data = self.serialize_morph(morph, *statdicts)
        except InitError as e:
            data = {"missingParams": e.init_params}
        except NotImplementedError:
            data = {"error": "INVALID_GAME"}
        except UnitNotFoundError:
            data = {"error": "UNIT_DNE"}
        return Response(data)

    def partial_update(self, request):
        """
        Simulates operations on a morph without modifying it.
        """
        morph_id = request.data.get("morph_id")
        if morph_id not in self.morphs:
            raise Exception
        morph = self.morphs[morph_id].copy()
        method = request.data.get("method")
        kwargs = request.data.get("kwargs")
        error = {
            "level_up": self.level_up,
            "promote": self.promote,
            "use_stat_booster": self.use_stat_booster,
            "use_afas_drops": self.use_afas_drops,
            "use_metiss_tome": self.use_metiss_tome,
            "equip_band": self.equip_band,
            "unequip_band": self.unequip_band,
            "equip_scroll": self.equip_scroll,
            "unequip_scroll": self.unequip_scroll,
        }[method](morph, **kwargs)
        # TODO: Refactor code s.t. stat formats are selected also.
        return self.serialize_morph(morph)

    def update(self, request):
        """
        Performs operations on a morph and modifies it.
        """
        morph_id = request.data.get("morph_id")
        if morph_id not in self.morphs:
            raise Exception
        morph = self.morphs[morph_id]
        method = request.data.get("method")
        kwargs = request.data.get("kwargs")
        error = {
            "level_up": self.level_up,
            "promote": self.promote,
            "use_stat_booster": self.use_stat_booster,
            "use_afas_drops": self.use_afas_drops,
            "use_metiss_tome": self.use_metiss_tome,
            "equip_band": self.equip_band,
            "unequip_band": self.unequip_band,
            "equip_scroll": self.equip_scroll,
            "unequip_scroll": self.unequip_scroll,
        }[method](morph, **kwargs)
        #statdicts = serializer(morph)
        # TODO: Refactor code s.t. stat formats are selected also.
        return self.serialize_morph(morph)

    def destroy(self, request, pk):
        """
        For deleting morph objects from the viewset.
        """
        status = {"success": None}
        try:
            self.morphs.pop(pk)
            status['success'] = True
        except KeyError as err:
            status['success'] = False
        logger.debug("Morph with id=%r has been deleted: %r", pk, status['success'])
        return Response(status)

    #level_up, promote, use_stat_booster, use_growths_item, equip_band, unequip_band, equip_scroll, unequip_scroll
    # NOTE: MORPH METHODS

    @staticmethod
    def level_up(morph, **kwargs):
        """
        Levels up a morph.
        """
        num_levels = int(kwargs.get("num_levels"))
        is_success: bool
        try:
            morph.level_up(num_levels)
            # get forecast stats.
            statdicts = self.serialize_current_stats(morph)
            if morph.growth_rates.has_been_augmented:
                statdicts.extend(self.serialize_level_up(morph, num_levels))
            else:
                statdicts.append((morph.growth_rates * 0.01).as_dict())
            value = self.serialize_morph(morph, *statdicts)
            is_success = True
        except LevelUpError as err:
            value = morph.max_level
            is_success = False
        return (is_success, value)

    @staticmethod
    def promote(morph, **kwargs):
        """
        Promotes a morph.
        """
        promo_cls = kwargs.get("promo_cls")
        morph.promo_cls = promo_cls
        is_success: bool
        try:
            value = morph.promote()
            is_success = True
        except PromotionError as err:
            value = err.promotion_list
            is_success = False
        return (is_success, value)

    # FE5,6,7,8,9
    @staticmethod
    def use_stat_booster(morph, **kwargs):
        """
        Uses a stat booster on a morph.
        """
        item_name = kwargs.get("item_name")
        is_success: bool
        try:
            morph.use_stat_booster(item_name)
            statdicts = self.serialize_current_stats(morph)
            value = self.serialize_morph(morph, *statdicts)
            is_success = True
        except StatBoosterError as err:
            value = err.valid_stat_boosters
            is_success = False
        return (is_success, value)

    # FE5
    @staticmethod
    def equip_scroll(morph, **kwargs):
        """
        Equips a growth-altering scroll onto on a morph. (FE5 only!)
        """
        old_growths = morph.growth_rates.as_dict()
        scroll_name = kwargs.get("scroll_name")
        is_success: bool
        try:
            morph.equip_scroll(scroll_name)
            value = self.serialize_growth_rates(morph)
            is_success = True
        except StatBoosterError as err:
            value = err.valid_scrolls
            is_success = False
        return (is_success, value)

    @staticmethod
    def unequip_scroll(morph, **kwargs):
        """
        Unequips a growth-altering scroll from a morph. (FE5 only!)
        """
        old_growths = morph.growth_rates.as_dict()
        scroll_name = kwargs.get("scroll_name")
        is_success: bool
        try:
            morph.unequip_scroll(scroll_name)
            value = self.serialize_growth_rates(morph)
            is_success = True
        except StatBoosterError as err:
            value = err.valid_scrolls
            is_success = False
        return (is_success, value)

    # FE7
    @staticmethod
    def use_afas_drops(morph, **kwargs):
        """
        Uses Afa's Drops on a morph. (FE7 only!)
        """
        is_success: bool
        old_growths = morph.growth_rates.as_dict()
        try:
            morph.use_afas_drops()
            value = self.serialize_growth_rates(morph)
            is_success = True
        except GrowthsItemError as err:
            value = None
            is_success = False
        return (is_success, value)

    # FE8
    @staticmethod
    def use_metiss_tome(morph, **kwargs):
        """
        Uses Metis' Tome on a morph. (FE8 only!)
        """
        is_success: bool
        old_growths = morph.growth_rates.as_dict()
        try:
            morph.use_metiss_drops()
            value = self.serialize_growth_rates(morph)
            is_success = True
        except GrowthsItemError as err:
            value = None
            is_success = False
        return (is_success, value)

    # FE8
    @staticmethod
    def equip_knight_ward(morph, **kwargs):
        """
        Equips the Knight Ward on a morph. (FE9 Knights only!)
        """
        is_success: bool
        old_growths = morph.growth_rates.as_dict()
        try:
            morph.equip_knight_ward()
            value = self.serialize_growth_rates(morph)
            is_success = True
        except GrowthsItemError as err:
            value = None
            is_success = False
        return (is_success, value)

    # FE8
    @staticmethod
    def unequip_knight_ward(morph, **kwargs):
        """
        Unequips the Knight Ward from a morph. (FE9 Knights only!)
        """
        is_success: bool
        old_growths = morph.growth_rates.as_dict()
        try:
            morph.equip_knight_ward()
            value = self.serialize_growth_rates(morph)
            is_success = True
        except GrowthsItemError as err:
            value = None
            is_success = False
        return (is_success, value)

    # FE9
    @staticmethod
    def equip_band(morph, **kwargs):
        """
        Equips a growth-altering band onto on a morph. (FE9 only!)
        """
        is_success: bool
        band_name = kwargs.get("band_name")
        old_growths = morph.growth_rates.as_dict()
        try:
            morph.equip_band(band_name)
            value = self.serialize_growth_rates(morph)
            is_success = True
        except BandError as err:
            value = err.valid_bands
            is_success = False
        return (is_success, value)

    @staticmethod
    def unequip_band(morph, **kwargs):
        """
        Unequips a growth-altering band from a morph. (FE9 only!)
        """
        band_name = kwargs.get("band_name")
        is_success: bool
        old_growths = morph.growth_rates.as_dict()
        try:
            morph.unequip_band(band_name)
            value = self.serialize_growth_rates(morph)
            is_success = True
        except BandError as err:
            value = err.valid_bands
            is_success = False
        return (is_success, value)

    # NOTE: SERIALIZERS

    @staticmethod
    def serialize_morph(morph, *statdicts):
        """
        Bundles a morph's attributes for display purposes.
        """
        stats = list(map(lambda stat: (stat, *map(lambda statdict: statdict[stat], statdicts)), morph.Stats.STAT_LIST()))
        return {
            "unitClass": morph.current_cls,
            "level": (morph.current_lv, morph.max_level),
            "stats": stats,
        }

    @staticmethod
    def serialize_current_stats(morph):
        """
        Bundles stats for default display-purposes.
        """
        current_stats = (morph.current_stats * 0.01).as_dict()
        max_stats = (morph.max_stats * 0.01).as_dict()
        absmax_stats = dict(zip(morph.Stats.STAT_LIST(), morph.Stats.ABSOLUTE_MAXES()))
        statdicts = [current_stats, max_stats, absmax_stats]
        return statdicts

    @staticmethod
    def serialize_growth_rates(morph):
        """
        Bundles growth augments for FE5, FE7, FE8, and FE9.
        """
        old_growths = (morph._og_growth_rates * 0.01).as_dict()
        new_growths = (morph.growth_rates * 0.01).as_dict()
        growths_diff = (morph.get_growth_augment() * 0.01).as_dict()
        statdicts = [old_growths, new_growths, growths_diff]
        return statdicts

    @staticmethod
    def serialize_level_up(morph, num_levels: int):
        """
        Bundles level-up stats for FE5, FE7, FE8, and FE9.
        """
        bonus_without_augment = (morph._og_growth_rates * num_levels * 0.01).as_dict()
        augment = (morph.get_growth_augment() * -num_levels * 0.01).as_dict()
        for stat in morph.Stats.ZERO_GROWTH_STAT_LIST():
            bonus_without_augment[stat] = None
            augment[stat] = None
        statdicts = [bonus_without_augment, augment]
        return statdicts

    # NOTE: ARGUMENT PARSERS

    @staticmethod
    def parse_init_args(dictlike):
        """
        Parses default values from response and converts them for interpretation by program.
        """
        game_no = int(dictlike.get("game_no"))
        name = dictlike.get("name")
        morph_options = (
            "father",
            "hard_mode",
            "number_of_declines",
            "route",
            "lyn_mode",
        )
        kwargs = {key: dictlike.get(key) for key in morph_options if dictlike.get(key) is not None}
        for kwarg, kwval in kwargs.items():
            if kwarg in ("hard_mode", "lyn_mode"):
                kwargs[kwarg] = {
                    "true": True,
                    "false": False,
                }[kwval]
            if kwarg == "number_of_declines":
                kwargs[kwarg] = int(kwval)
        return (game_no, name, kwargs)

