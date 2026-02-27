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

    def test_init__fail(self):
        """
        """
        self.kwargs['father'] = ""
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

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

    def test_init__fail(self):
        """
        """
        self.kwargs['hard_mode'] = "???"
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

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

    def test_init__fail(self):
        """
        """
        self.kwargs['number_of_declines'] = -4
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

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

    def test_init__fail(self):
        """
        """
        self.kwargs['route'] = "A"
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)


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

    def test_init__fail(self):
        """
        """
        self.kwargs['lyn_mode'] = "A"
        serializer = InitArgs(data=self.kwargs)
        actual = serializer.is_valid()
        expected = False
        self.assertIs(actual, expected)

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


