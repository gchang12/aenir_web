"""
"""

import unittest
from unittest.mock import patch

from django.test import TestCase
from django.core.exceptions import ValidationError

from aenir_web._logging import logger

from dracogate.models import VirtualMorph

class NormalUnit(TestCase):
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
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'])

    def test_level_up(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        num_levels = 19
        with patch("aenir.morph.Morph.level_up") as MOCK_level_up:
            vmorph.level_up(num_levels=num_levels)
        MOCK_level_up.assert_called_once_with(num_levels)
        actual = vmorph.history
        expected = [("level_up", {"num_levels": num_levels})]
        self.assertListEqual(actual, expected)
        logger.debug("Checking to see if any errors are raised.")
        vmorph.init()

    def test_level_up__no_simulate(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        num_levels = 19
        vmorph.level_up(num_levels=num_levels)
        self.assertTrue(vmorph.history)
        vmorph.save()
        morph = VirtualMorph.objects.get().init()
        actual = morph.current_lv
        expected = 20
        self.assertEqual(actual, expected)

    def test_promote(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        promo_cls = None
        with patch("aenir.morph.Morph.promote") as MOCK_promote:
            vmorph.promote(promo_cls=promo_cls)
        MOCK_promote.assert_called_once_with()
        actual = vmorph.history
        expected = [("promote", {"promo_cls": promo_cls})]
        self.assertListEqual(actual, expected)
        logger.debug("Checking to see if any errors are raised.")
        morph = vmorph.init()

    def test_promote__no_simulate(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        promo_cls = None
        vmorph.promote(promo_cls=promo_cls)
        self.assertTrue(vmorph.history)
        vmorph.save()
        morph = VirtualMorph.objects.get().init()
        actual = morph.current_cls
        expected = "Master Lord"
        self.assertEqual(actual, expected)

    def test_use_stat_booster(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        vmorph.init()
        item_name = "Angelic Robe"
        #with patch("dracogate.models.Morph.use_stat_booster") as MOCK_use_stat_booster:
        with patch("aenir.morph.Morph.use_stat_booster") as MOCK_use_stat_booster:
            vmorph.use_stat_booster(item_name=item_name)
        MOCK_use_stat_booster.assert_called_once_with(item_name)
        actual = vmorph.history
        expected = [("use_stat_booster", {"item_name": item_name})]
        self.assertListEqual(actual, expected)
        logger.debug("Checking to see if any errors are raised.")
        vmorph.init()

    def test_use_stat_booster__no_simulate(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        logger.debug("This test is being run with the assumption that 'init' works.")
        morph = vmorph.init()
        og_hp = morph.current_stats.HP
        item_name = "Angelic Robe"
        #with patch("dracogate.models.Morph.use_stat_booster") as MOCK_use_stat_booster:
        vmorph.use_stat_booster(item_name=item_name)
        self.assertTrue(vmorph.history)
        vmorph.save()
        morph2 = VirtualMorph.objects.get().init()
        expected = og_hp + 7_00
        actual = morph2.current_stats.HP
        self.assertEqual(actual, expected)

class FatheredUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "FatheredUnit"
        kwargs = {'game_no': 4, "name": "Lakche", "options": {"father": "Lex"}}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        self.options = kwargs.pop('options')
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        kwargs = self.kwargs
        options = self.options
        vmorph = self.vmorph
        with patch("aenir.morph.Morph4") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], father=options['father'])

class HardModeUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "HardModeUnit"
        kwargs = {'game_no': 6, "name": "Rutger", "options": {"hard_mode": True}}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        self.options = kwargs.pop('options')
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        kwargs = self.kwargs
        options = self.options
        vmorph = self.vmorph
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], hard_mode=options['hard_mode'])

class DeclinableUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "DeclinableUnit"
        kwargs = {'game_no': 6, "name": "Hugh", "options": {"number_of_declines": True}}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        self.options = kwargs.pop('options')
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        kwargs = self.kwargs
        options = self.options
        vmorph = self.vmorph
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], number_of_declines=options['number_of_declines'])

class Gonzales(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "Gonzales"
        kwargs = {'game_no': 6, "name": "Gonzales", "options": {"hard_mode": False, "route": "Lalum"}}
        self.options = kwargs.pop('options')
        self.kwargs = kwargs
        self.morph_id = morph_id

    def test_init(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], hard_mode=options['hard_mode'], route=options['route'])

    def test_init__lalum_hm(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        options['hard_mode'] = True
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], hard_mode=options['hard_mode'], route=options['route'])

    def test_init__elphin(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        options['route'] = "Elphin"
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], hard_mode=options['hard_mode'], route=options['route'])

    def test_init__elphin_hm(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        options['route'] = "Elphin"
        options['hard_mode'] = True
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], hard_mode=options['hard_mode'], route=options['route'])

class LyndisLeague(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {'game_no': 7, "name": "Lyn", "options": {"lyn_mode": False}}
        morph_id = "LyndisLeague"
        self.options = kwargs.pop('options')
        self.kwargs = kwargs
        self.morph_id = morph_id

    def test_init(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("aenir.morph.Morph7") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], lyn_mode=False)

    def test_init__lyn_mode(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        options['lyn_mode'] = True
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with patch("aenir.morph.Morph7") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with(kwargs['name'], lyn_mode=True)

class Ninian(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

class Nils(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

class CreatureCampaignUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

class ThracianUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "ThracianMorph"
        kwargs = {'game_no': 5, "name": "Leaf"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

class ElibeanUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "ElibeanMorph"
        kwargs = {'game_no': 7, "name": "Eliwood"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

class SacredStonesUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "ElibeanMorph"
        kwargs = {'game_no': 8, "name": "Seth"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

class TelliusKnightUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "ElibeanMorph"
        kwargs = {'game_no': 9, "name": "Kieran"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

