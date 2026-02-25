"""
"""

import unittest
from unittest.mock import patch

from django.test import TestCase
from django.core.exceptions import ValidationError

from aenir_web._logging import logger

from dracogate.models import VirtualMorph

class NormalMorph(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.morph_id = "NormalMorph"
        self.kwargs = {'game_no': 6, "name": "Roy"}

    def test_default_values(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **self.kwargs)
        actual = vmorph.options
        expected = {}
        logger.debug("vmorph.options: %r", vmorph.options)
        self.assertDictEqual(actual, expected)
        actual = vmorph.history
        expected = []
        logger.debug("vmorph.history: %r", vmorph.history)
        self.assertListEqual(actual, expected)
        actual = vmorph.user
        self.assertIsNone(actual)

    def test_two_morphs_with_same_id_can_coexist_if_user_is_null(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        morph1 = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        morph2 = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        actual = VirtualMorph.objects.filter(morph_id=morph_id).count()
        expected = 2
        self.assertEqual(actual, expected)
        morph1.full_clean()
        morph2.full_clean()

    def test_morph_can_have_blank_morph_id(self):
        """
        """
        morph_id = ""
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with self.assertRaises(ValidationError):
            vmorph.full_clean()
        logger.debug("At the model level, a Morph object can have a blank 'morph_id' value; not so much at the form level.")

    def test_morph_cannot_have_blank_name(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        kwargs['name'] = ""
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with self.assertRaises(ValidationError):
            vmorph.full_clean()
        logger.debug("At the model level, a Morph object can have a blank 'name' value; not so much at the form level.")

    def test_init(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("dracogate.models.get_morph") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['game_no'], kwargs['name'])

    def test_level_up(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        num_levels = 19
        with patch("dracogate.models.Morph.level_up") as MOCK_level_up:
            vmorph.level_up(num_levels=num_levels)
        MOCK_level_up.assert_called_once_with(num_levels)

    def test_promote(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        promo_cls = None
        with patch("dracogate.models.Morph.promote") as MOCK_promote:
            vmorph.promote(promo_cls=promo_cls)
        MOCK_promote.assert_called_once_with()

    def test_use_stat_booster(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        item_name = "Angelic Robe"
        with patch("dracogate.models.Morph.use_stat_booster") as MOCK_use_stat_booster:
            vmorph.use_stat_booster(item_name=item_name)
        MOCK_use_stat_booster.assert_called_once_with(item_name)

class FatheredUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class HardModeUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class DeclinableUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class Gonzales(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class LyndisLeague(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class Ninian(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class Nils(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

class CreatureCampaignUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def tearDown(self):
        """
        """

