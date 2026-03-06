"""
"""

import unittest
from unittest.mock import patch

from django.test import TestCase
from django.core.exceptions import ValidationError

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

from dracogate.serializers import (
    InitArgs,
    LevelUpArgs,
    PromoteArgs,
    UseStatBoosterArgs,
    ScrollEquipmentArgs,
    BandEquipmentArgs,
    MorphMethodArgs,
    MorphIDSerializer,
    # custom
    MorphSerializer,
    NullDictSerializer,
)
from dracogate._logging import logger

class NormalUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 6, "name": "Roy"}
        options = {}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_init__fail(self):
        """
        """
        self.kwargs['game_no'] = 10
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_parse_init_args(self):
        """
        """
        expected = (self.kwargs['game_no'], self.kwargs['name'], {})
        self.kwargs['game_no'] = str(self.kwargs['game_no'])
        actual = MorphSerializer.parse_init_args(self.kwargs)
        self.assertTupleEqual(actual, expected)

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_parse_init_args__nonint_game_no(self):
        """
        """
        self.kwargs['game_no'] = ""
        expected = (self.kwargs['game_no'], self.kwargs['name'], {})
        #self.kwargs['game_no'] = str(self.kwargs['game_no'])
        with self.assertRaises(ValueError):
            MorphSerializer.parse_init_args(self.kwargs)
        #self.assertTupleEqual(actual, expected)

    def test_get_current_stats(self):
        """
        """
        morph = get_morph(**self.kwargs)
        serializer = MorphSerializer(morph)
        expected = [
            {
                "HP": 18.0,
                "Pow": 5.0,
                "Skl": 5.0,
                "Spd": 7.0,
                "Lck": 7.0,
                "Def": 5.0,
                "Res": 0.0,
                "Con": 6.0,
                "Mov": 5.0,
            },
            {
                "HP": 60.0,
                "Pow": 20.0,
                "Skl": 20.0,
                "Spd": 20.0,
                "Lck": 30.0,
                "Def": 20.0,
                "Res": 20.0,
                "Con": 20.0,
                "Mov": 15.0,
            },
            {
                "HP": 80.0,
                "Pow": 30.0,
                "Skl": 30.0,
                "Spd": 30.0,
                "Lck": 30.0,
                "Def": 30.0,
                "Res": 30.0,
                "Con": 25.0,
                "Mov": 15.0,
            },
        ]
        actual = list(serializer.get_current_stats())
        logger.debug("actual: %r", actual)
        logger.debug("expected: %r", expected)
        self.assertListEqual(actual, expected)

    def test_get_morph(self):
        """
        """
        current_stats = {
            "HP": 18.0,
            "Pow": 5.0,
            "Skl": 5.0,
            "Spd": 7.0,
            "Lck": 7.0,
            "Def": 5.0,
            "Res": 0.0,
            "Con": 6.0,
            "Mov": 5.0,
        }
        max_stats = {
            "HP": 60.0,
            "Pow": 20.0,
            "Skl": 20.0,
            "Spd": 20.0,
            "Lck": 30.0,
            "Def": 20.0,
            "Res": 20.0,
            "Con": 20.0,
            "Mov": 15.0,
        }
        global_max_stats = {
            "HP": 80.0,
            "Pow": 30.0,
            "Skl": 30.0,
            "Spd": 30.0,
            "Lck": 30.0,
            "Def": 30.0,
            "Res": 30.0,
            "Con": 25.0,
            "Mov": 15.0,
        }
        statdicts = (current_stats, max_stats, global_max_stats)
        morph = get_morph(**self.kwargs)
        morph._set_max_level()
        serializer = MorphSerializer(morph)
        actual = serializer.get_morph(*statdicts)
        expected = {
            "stats": [
                ("HP", 18.0, 60.0, 80.0),
                ("Pow", 5.0, 20.0, 30.0),
                ("Skl", 5.0, 20.0, 30.0),
                ("Spd", 7.0, 20.0, 30.0),
                ("Lck", 7.0, 30.0, 30.0),
                ("Def", 5.0, 20.0, 30.0),
                ("Res", 0.0, 20.0, 30.0),
                ("Con", 6.0, 20.0, 25.0),
                ("Mov", 5.0, 15.0, 15.0),
            ],
            "level": (1, 20),
            "unitClass": "Lord",
        }
        self.assertDictEqual(actual, expected)

class GrowthRates(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.kwargs = {"game_no": 7, "name": "Eliwood"}
        # Eliwood
        self.stats = {
            "growths": {
                "HP": 80,
                "Pow": 45,
                "Skl": 50,
                "Spd": 40,
                "Lck": 45,
                "Def": 30,
                "Res": 35,
                "Con": None,
                "Mov": None,
            },
            1: {
                "HP": 18_00,
                "Pow": 5_00,
                "Skl": 5_00,
                "Spd": 7_00,
                "Lck": 7_00,
                "Def": 5_00,
                "Res": 0,
                "Con": 7_00,
                "Mov": 5_00,
            },
            2: {
                "HP": 18_80,
                "Pow": 5_45,
                "Skl": 5_50,
                "Spd": 7_40,
                "Lck": 7_45,
                "Def": 5_30,
                "Res": 35,
                "Con": 7_00,
                "Mov": 5_00,
            },
            20: {
                "HP": 33_20,
                "Pow": 13_55,
                "Skl": 14_50,
                "Spd": 14_60,
                "Lck": 15_55,
                "Def": 10_70,
                "Res": 6_65,
                "Con": 7_00,
                "Mov": 5_00,
            },
        }

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_get_growth_rates(self):
        """
        """
        expected = [
            {
                "HP": 80,
                "Pow": 45,
                "Skl": 50,
                "Spd": 40,
                "Lck": 45,
                "Def": 30,
                "Res": 35,
                "Con": None,
                "Mov": None,
            },
            {
                "HP": 85,
                "Pow": 50,
                "Skl": 55,
                "Spd": 45,
                "Lck": 50,
                "Def": 35,
                "Res": 40,
                "Con": None,
                "Mov": None,
            },
        ]
        morph = get_morph(**self.kwargs)
        morph.use_afas_drops()
        serializer = MorphSerializer(morph)
        actual = list(serializer.get_growth_rates())
        self.assertListEqual(actual, expected)

    def test_get_level_up_bonuses_with_augment(self):
        """
        """
        num_levels = 19
        expected = [
            {
                "HP": 15.20,
                "Pow": 8.55,
                "Skl": 9.50,
                "Spd": 7.60,
                "Lck": 8.55,
                "Def": 5.70,
                "Res": 6.65,
                "Con": None,
                "Mov": None,
            },
            {
                "HP": 0.95,
                "Pow": 0.95,
                "Skl": 0.95,
                "Spd": 0.95,
                "Lck": 0.95,
                "Def": 0.95,
                "Res": 0.95,
                "Con": None,
                "Mov": None,
            },
        ]
        morph = get_morph(**self.kwargs)
        morph.use_afas_drops()
        serializer = MorphSerializer(morph)
        actual = list(serializer.get_level_up_bonuses_with_augment(num_levels))
        self.assertListEqual(actual, expected)

    def test_nullify_zero_growth_rates(self):
        """
        """
        morph = get_morph(**self.kwargs)
        serializer = MorphSerializer(morph)
        dictlike = {
            "HP": 0.80,
            "Pow": 0.45,
            "Skl": 0.50,
            "Spd": 0.40,
            "Lck": 0.45,
            "Def": 0.30,
            "Res": 0.35,
            "Con": 0.0,
            "Mov": 0.0,
        }
        actual = serializer.nullify_zero_growth_stats(dictlike)
        expected = {
            "HP": 0.80,
            "Pow": 0.45,
            "Skl": 0.50,
            "Spd": 0.40,
            "Lck": 0.45,
            "Def": 0.30,
            "Res": 0.35,
            "Con": None,
            "Mov": None,
        }
        self.assertDictEqual(actual, expected)

    def test_divide_by_100(self):
        """
        """
        growth_rates = self.stats['growths']
        expected = {
            "HP": 0.80,
            "Pow": 0.45,
            "Skl": 0.50,
            "Spd": 0.40,
            "Lck": 0.45,
            "Def": 0.30,
            "Res": 0.35,
            "Con": None,
            "Mov": None,
        }
        actual = MorphSerializer.divide_by_100(growth_rates)
        self.assertDictEqual(actual, expected)

    def test_divide_by_100__str_value(self):
        """
        """
        growth_rates = self.stats['growths']
        growth_rates['HP'] = "100"
        with self.assertRaises(TypeError):
            MorphSerializer.divide_by_100(growth_rates)

class FatheredUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 4, "name": "Lakche"}
        options = {"father": "Lex"}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_init__fail(self):
        """
        """
        self.kwargs['father'] = ""
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_parse_init_args(self):
        """
        """
        expected = (self.kwargs['game_no'], self.kwargs['name'], {"father": "Lex"})
        self.kwargs['game_no'] = str(self.kwargs['game_no'])
        actual = MorphSerializer.parse_init_args(self.kwargs)
        self.assertTupleEqual(actual, expected)

class HardModeUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 6, "name": "Rutger"}
        options = {"hard_mode": "false"}
        kwargs.update(options)
        self.kwargs = kwargs


    def test_init(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        expected['hard_mode'] = False
        self.assertDictEqual(actual, expected)

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        expected['hard_mode'] = False
        self.assertDictEqual(actual, expected)

    def test_init__fail(self):
        """
        """
        self.kwargs['hard_mode'] = "???"
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_parse_init_args(self):
        """
        """
        expected = (self.kwargs['game_no'], self.kwargs['name'], {"hard_mode": False})
        actual = MorphSerializer.parse_init_args(self.kwargs)
        self.assertTupleEqual(actual, expected)

class DeclinableUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 6, "name": "Hugh"}
        options = {"number_of_declines": 0}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_init__fail(self):
        """
        """
        self.kwargs['number_of_declines'] = -4
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_parse_init_args(self):
        """
        """
        expected = (self.kwargs['game_no'], self.kwargs['name'], {"number_of_declines": 0})
        self.kwargs['number_of_declines'] = "0"
        actual = MorphSerializer.parse_init_args(self.kwargs)
        self.assertTupleEqual(actual, expected)

    def test_parse_init_args(self):
        """
        """
        self.kwargs['game_no'] = ""
        expected = (self.kwargs['game_no'], self.kwargs['name'], {})
        #self.kwargs['game_no'] = str(self.kwargs['game_no'])
        with self.assertRaises(ValueError):
            MorphSerializer.parse_init_args(self.kwargs)
        #self.assertTupleEqual(actual, expected)

    def test_parse_init_args__nonint_number_of_declines(self):
        """
        """
        self.kwargs['number_of_declines'] = ""
        expected = (str(self.kwargs['game_no']), self.kwargs['name'], {"number_of_declines": ""})
        #self.kwargs['number_of_declines'] = "0"
        with self.assertRaises(ValueError):
            actual = MorphSerializer.parse_init_args(self.kwargs)
        #self.assertTupleEqual(actual, expected)

class Gonzales(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 6, "name": "Gonzales"}
        options = {"hard_mode": "false", "route": "Lalum"}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        expected['hard_mode'] = False
        self.assertDictEqual(actual, expected)

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        expected['hard_mode'] = False
        self.assertDictEqual(actual, expected)

    def test_init__fail(self):
        """
        """
        self.kwargs['route'] = "A"
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_parse_init_args(self):
        """
        """
        expected = (self.kwargs['game_no'], self.kwargs['name'], {"hard_mode": False, "route": "Lalum"})
        actual = MorphSerializer.parse_init_args(self.kwargs)
        self.assertTupleEqual(actual, expected)

class LyndisLeague(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 7, "name": "Lyn"}
        options = {"lyn_mode": "false"}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        expected['lyn_mode'] = False
        self.assertDictEqual(actual, expected)

    def test_init__with_serializer(self):
        """
        """
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.kwargs
        expected['lyn_mode'] = False
        self.assertDictEqual(actual, expected)

    def test_init__fail(self):
        """
        """
        self.kwargs['lyn_mode'] = "A"
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_parse_init_args(self):
        """
        """
        expected = (self.kwargs['game_no'], self.kwargs['name'], {"lyn_mode": False})
        actual = MorphSerializer.parse_init_args(self.kwargs)
        self.assertTupleEqual(actual, expected)

class LevelUpIncrements(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.kwargs = {"num_levels": 0}

    def test_0(self):
        """
        """
        serializer = LevelUpArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_20(self):
        """
        """
        self.kwargs['num_levels'] = 20
        serializer = LevelUpArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_21(self):
        """
        """
        self.kwargs['num_levels'] = 21
        serializer = LevelUpArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_null_data(self):
        """
        """
        self.kwargs.clear()
        serializer = LevelUpArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

class PromotionClasses(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.kwargs = {"promo_cls": None}

    def test_null(self):
        """
        """
        serializer = PromoteArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_null_str(self):
        """
        """
        self.kwargs['promo_cls'] = ''
        serializer = PromoteArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)
        #actual = serializer.validated_data
        #expected = self.kwargs
        #self.assertDictEqual(actual, expected)

    def test_nonnull_str(self):
        """
        """
        self.kwargs['promo_cls'] = 'Master Lord'
        serializer = PromoteArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_null_data(self):
        """
        """
        self.kwargs.clear()
        serializer = PromoteArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

class StatBoosters(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.kwargs = {"item_name": None}

    def test_null_data(self):
        """
        """
        self.kwargs.clear()
        serializer = UseStatBoosterArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_non_stat_booster(self):
        """
        """
        self.kwargs['item_name'] = 'Master Lord'
        serializer = UseStatBoosterArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_stat_booster(self):
        """
        """
        self.kwargs['item_name'] = 'Angelic Robe'
        serializer = UseStatBoosterArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

class Scrolls(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.kwargs = {"scroll_name": None}

    def test_non_scroll(self):
        """
        """
        self.kwargs['scroll_name'] = 'Eliwood'
        serializer = ScrollEquipmentArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_scroll(self):
        """
        """
        self.kwargs['scroll_name'] = 'Odo'
        serializer = ScrollEquipmentArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

    def test_null_data(self):
        """
        """
        self.kwargs.clear()
        serializer = ScrollEquipmentArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

class Bands(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.kwargs = {"band_name": None}

    def test_null_data(self):
        """
        """
        self.kwargs.clear()
        serializer = BandEquipmentArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_non_band(self):
        """
        """
        self.kwargs['band_name'] = 'Eliwood'
        serializer = BandEquipmentArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

    def test_band(self):
        """
        """
        self.kwargs['band_name'] = 'Sword Band'
        serializer = BandEquipmentArgs(data=self.kwargs)
        serializer.is_valid()
        actual = serializer.validated_data
        expected = self.kwargs
        self.assertDictEqual(actual, expected)

class MorphMethods(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def test_level_up(self):
        """
        """
        data = {"method_name": "level_up", "args": {"num_levels": 0}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_promote(self):
        """
        """
        data = {"method_name": "promote", "args": {"promo_cls": "Master Lord"}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_use_stat_booster(self):
        """
        """
        data = {"method_name": "use_stat_booster", "args": {"item_name": "Angelic Robe"}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_equip_scroll(self):
        """
        """
        data = {"method_name": "equip_scroll", "args": {"scroll_name": "Odo"}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_unequip_scroll(self):
        """
        """
        data = {"method_name": "unequip_scroll", "args": {"scroll_name": "Odo"}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_use_afas_drops(self):
        """
        """
        data = {"method_name": "use_afas_drops", "args": {}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)
        null_dict_serializer = NullDictSerializer(data=data.pop("args"))
        actual = null_dict_serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = null_dict_serializer.validated_data
        expected = {}
        self.assertDictEqual(actual, expected)

    def test_use_metiss_tome(self):
        """
        """
        data = {"method_name": "use_metiss_tome", "args": {}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)
        null_dict_serializer = NullDictSerializer(data=data.pop("args"))
        actual = null_dict_serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = null_dict_serializer.validated_data
        expected = {}
        self.assertDictEqual(actual, expected)

    def test_equip_band(self):
        """
        """
        data = {"method_name": "equip_band", "args": {"band_name": "Sword Band"}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_unequip_band(self):
        """
        """
        data = {"method_name": "unequip_band", "args": {"band_name": "Sword Band"}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_invalid_method(self):
        """
        """
        data = {"method_name": "levelUp", "args": {"num_levels": 0}}
        serializer = MorphMethodArgs(data=data)
        expected = False
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        # expected failure
        actual = serializer.validated_data
        expected = {}
        self.assertDictEqual(actual, expected)

    def test_invalid_args(self):
        """
        """
        data = {"method_name": "level_up", "args": None}
        serializer = MorphMethodArgs(data=data)
        expected = False
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        # expected failure
        actual = serializer.validated_data
        expected = {}
        self.assertDictEqual(actual, expected)

    def test_equip_knight_ward(self):
        """
        """
        data = {"method_name": "equip_knight_ward", "args": {}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        # expected failure
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

    def test_unequip_knight_ward(self):
        """
        """
        data = {"method_name": "unequip_knight_ward", "args": {}}
        serializer = MorphMethodArgs(data=data)
        expected = True
        actual = serializer.is_valid()
        self.assertIs(actual, expected)
        # expected failure
        actual = serializer.validated_data
        expected = data
        self.assertDictEqual(actual, expected)

class MorphID(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.data = {"morph_id": None}

    def test_less_than_26_chars(self):
        """
        """
        num_chars = 25
        morph_id = "".join([letter for letter in ("a" for _ in range(num_chars))])
        self.data['morph_id'] = morph_id
        serializer = MorphIDSerializer(data=self.data)
        actual = serializer.is_valid()
        expected = True
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = self.data
        self.assertDictEqual(actual, expected)

    def test_26_or_more_chars(self):
        """
        """
        num_chars = 26
        morph_id = "".join([letter for letter in ("a" for _ in range(num_chars))])
        self.data['morph_id'] = morph_id
        serializer = MorphIDSerializer(data=self.data)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)
        actual = serializer.validated_data
        expected = {}
        self.assertDictEqual(actual, expected)

