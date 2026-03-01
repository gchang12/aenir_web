"""
"""

import unittest
from unittest.mock import patch

from django.test import TestCase
from django.core.exceptions import ValidationError

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

from dracogate.models import VirtualMorph

class InitTest(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        self.morph_id = "InitTest"
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

class NormalUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "NormalUnit"
        kwargs = {'game_no': 6, "name": "Roy"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Roy")

    def test_level_up(self):
        """
        """
        vmorph = self.vmorph
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
        vmorph = self.vmorph
        vmorph.init()
        num_levels = 19
        (is_success, _) = vmorph.level_up(num_levels=num_levels)
        self.assertIs(is_success, True)
        self.assertTrue(vmorph.history)
        vmorph.save()
        morph = VirtualMorph.objects.get().init()
        actual = morph.current_lv
        expected = 20
        self.assertEqual(actual, expected)

    def test_promote(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with patch("aenir.morph.Morph.promote") as MOCK_promote:
            vmorph.promote(promo_cls=None)
        MOCK_promote.assert_called_once_with(promo_cls=None)
        actual = vmorph.history
        expected = [("promote", {"promo_cls": None})]
        self.assertListEqual(actual, expected)
        logger.debug("Checking to see if any errors are raised.")
        morph = vmorph.init()

    def test_promote__no_simulate(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        promo_cls = None
        (is_success, actual) = vmorph.promote(promo_cls=promo_cls)
        self.assertIs(is_success, True)
        expected = [(1, "Master Lord")]
        self.assertEqual(actual, expected)
        self.assertTrue(vmorph.history)
        vmorph.save()
        morph = VirtualMorph.objects.get().init()

    def test_use_stat_booster(self):
        """
        """
        vmorph = self.vmorph
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
        vmorph = self.vmorph
        morph = vmorph.init()
        og_hp = morph.current_stats.HP
        item_name = "Angelic Robe"
        #with patch("dracogate.models.Morph.use_stat_booster") as MOCK_use_stat_booster:
        (is_success, _) = vmorph.use_stat_booster(item_name=item_name)
        self.assertIs(is_success, True)
        self.assertTrue(vmorph.history)
        vmorph.save()
        morph2 = VirtualMorph.objects.get().init()
        expected = og_hp + 7_00
        actual = morph2.current_stats.HP
        self.assertEqual(actual, expected)

    def test_level_up__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        expected = (2, 20)
        (is_success, actual) = vmorph.level_up(num_levels=0)
        self.assertTupleEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_level_up__exceeds_max(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.level_up(num_levels=19)
        self.assertIs(is_success, True)
        expected = [2, 20]
        self.assertListEqual(actual, expected)
        (is_success, actual) = vmorph.level_up(num_levels=1)
        self.assertIs(is_success, False)
        expected = 20
        self.assertEqual(actual, expected)
        expected = [
            ("level_up", {"num_levels": 19}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)

    def test_promote__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.promote(promo_cls=None)
        expected = [(1, "Master Lord")]
        self.assertListEqual(actual, expected)
        expected = [
            ("promote", {"promo_cls": None}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, True)

    def test_use_stat_booster__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.use_stat_booster(item_name="")
        expected = (
            "Angelic Robe",
            "Energy Ring",
            "Secret Book",
            "Speedwings",
            "Goddess Icon",
            "Dragonshield",
            "Talisman",
            "Boots",
            "Body Ring",
        )
        self.assertTupleEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_use_stat_booster__stat_is_maxed(self):
        """
        """
        vmorph = self.vmorph
        morph = vmorph.init()
        morph.current_stats.HP = 60_00
        (is_success, actual) = vmorph.use_stat_booster(item_name="Angelic Robe")
        expected = ("HP", 60_00)
        self.assertTupleEqual(actual, expected)
        self.assertIs(is_success, False)

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
        vmorph = self.vmorph
        with patch("aenir.morph.Morph4") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Lakche", father="Lex")

    def test_use_stat_booster(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.use_stat_booster(item_name="Angelic Robe")

    def test_equip_scroll(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.equip_scroll(scroll_name="Odo")

    def test_unequip_scroll(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.unequip_scroll(scroll_name="Odo")

    def test_use_afas_drops(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.use_afas_drops()

    def test_use_metiss_tome(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.use_metiss_tome()

    def test_equip_knight_ward(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.equip_knight_ward()

    def test_unequip_knight_ward(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.unequip_knight_ward()

    def test_equip_band(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.equip_band(band_name="Sword Band")

    def test_unequip_band(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        with self.assertRaises(NotImplementedError):
            vmorph.unequip_band(band_name="Sword Band")


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
        vmorph = self.vmorph
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Rutger", hard_mode=True)

class DeclinableUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "DeclinableUnit"
        kwargs = {'game_no': 6, "name": "Hugh", "options": {"number_of_declines": 3}}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        self.options = kwargs.pop('options')
        self.kwargs = kwargs

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph6") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Hugh", number_of_declines=3)

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
        MOCK_get_morph.assert_called_once_with("Lyn", lyn_mode=False)

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
        MOCK_get_morph.assert_called_once_with("Lyn", lyn_mode=True)

class Ninian(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {'game_no': 7, "name": "Ninian", "options": {"lyn_mode": False}}
        morph_id = "Ninian"
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
        MOCK_get_morph.assert_called_once_with("Ninian", lyn_mode=False)

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
        MOCK_get_morph.assert_called_once_with("Ninian", lyn_mode=True)

    def test_init__lyn_mode__no_simulation(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        options = self.options
        options['lyn_mode'] = True
        kwargs["options"] = options
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        with self.assertRaises(UnitNotFoundError):
            vmorph.init()

    def test_promote__no_promotions(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)
        vmorph.init()
        vmorph.morph._set_max_level()
        vmorph.level_up(num_levels=19)
        (is_success, actual) = vmorph.promote(promo_cls="")
        self.assertIs(is_success, False)
        self.assertIsNone(actual)
        #expected = []
        #self.assertListEqual(actual, expected)
        actual = vmorph.history
        expected = [
            ("level_up", {"num_levels": 19}),
        ]
        self.assertListEqual(actual, expected)

class Nils(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {'game_no': 7, "name": "Nils", "options": {"lyn_mode": False}}
        morph_id = "Nils"
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
        MOCK_get_morph.assert_called_once_with("Nils", lyn_mode=False)

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
        MOCK_get_morph.assert_called_once_with("Nils", lyn_mode=True)

class CreatureCampaignUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {'game_no': 8, "name": "Lyon"}
        morph_id = "CreatureCampaignUnit"
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph8") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Lyon")

    def test_level_up(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, _) = vmorph.level_up(num_levels=20 - vmorph.morph.current_lv)
        self.assertIs(is_success, True)
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        morph = vmorph2.init()
        with self.assertRaises(LevelUpError):
            morph.level_up(1)


class ThracianUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "ThracianUnit"
        kwargs = {'game_no': 5, "name": "Leaf"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph5") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Leaf")

    def test_equip_scroll(self):
        """
        """
        scroll_name = "Odo"
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_scroll(scroll_name=scroll_name)
        self.assertIs(is_success, True)
        self.assertIsNone(actual)
        # check history
        expected = [
            ("equip_scroll", {"scroll_name": scroll_name}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        # refetch
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        vmorph2.init()
        (is_success, actual) = vmorph2.equip_scroll(scroll_name=scroll_name)
        expected = {
            "Odo": False,
            "Baldo": True,
            "Hezul": True,
            "Dain": True,
            "Noba": True,
            "Neir": True,
            "Ulir": True,
            "Tordo": True,
            "Fala": True,
            "Sety": True,
            "Blaggi": True,
            "Heim": True,
        }
        self.assertDictEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_unequip_scroll(self):
        """
        """
        scroll_name = "Odo"
        vmorph = self.vmorph
        vmorph.init()
        (is_success, _) = vmorph.equip_scroll(scroll_name=scroll_name)
        self.assertIs(is_success, True)
        (is_success, _) = vmorph.unequip_scroll(scroll_name=scroll_name)
        self.assertIs(is_success, True)
        expected = [
            ("equip_scroll", {"scroll_name": scroll_name}),
            ("unequip_scroll", {"scroll_name": scroll_name}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        vmorph2.init()
        expected = [
            ["equip_scroll", {"scroll_name": scroll_name}],
            ["unequip_scroll", {"scroll_name": scroll_name}],
        ]
        actual = vmorph2.history
        self.assertListEqual(actual, expected)


    def test_equip_scroll__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_scroll(scroll_name="")
        expected = {
            'Baldo': True,
            'Blaggi': True,
            'Dain': True,
            'Fala': True,
            'Heim': True,
            'Hezul': True,
            'Neir': True,
            'Noba': True,
            'Odo': True,
            'Sety': True,
            'Tordo': True,
            'Ulir': True,
        }
        self.assertDictEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    #@unittest.skip("I already have a means of determining what scrolls I've got on a unit.")
    def test_unequip_scroll__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.unequip_scroll(scroll_name="")
        self.assertIs(is_success, False)
        expected = {
            'Baldo': False,
            'Blaggi': False,
            'Dain': False,
            'Fala': False,
            'Heim': False,
            'Hezul': False,
            'Neir': False,
            'Noba': False,
            'Odo': False,
            'Sety': False,
            'Tordo': False,
            'Ulir': False,
        }
        self.assertDictEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)

class ElibeanUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "ElibeanUnit"
        kwargs = {'game_no': 7, "name": "Eliwood"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph7") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Eliwood")

    def test_use_afas_drops(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.use_afas_drops()
        self.assertIs(is_success, True)
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        vmorph2.init()
        (is_success, actual) = vmorph2.use_afas_drops()
        self.assertIsNotNone(actual)
        expected = [
            ["use_afas_drops", {}],
        ]
        actual = vmorph2.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_use_afas_drops__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, _) = vmorph.use_afas_drops()
        self.assertIs(is_success, True)
        (is_success, actual) = vmorph.use_afas_drops()
        self.assertIs(is_success, False)
        expected = (1, "Lord")
        self.assertTupleEqual(actual, expected)
        expected = [
            ("use_afas_drops", {}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)

class SacredStonesUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "SacredStonesUnit"
        kwargs = {'game_no': 8, "name": "Ephraim"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph8") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Ephraim")

    def test_use_metiss_tome(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, _) = vmorph.use_metiss_tome()
        self.assertIs(is_success, True)
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        vmorph2.init()
        (is_success, actual) = vmorph2.use_metiss_tome()
        self.assertIsNotNone(actual)
        expected = [
            ["use_metiss_tome", {}],
        ]
        actual = vmorph2.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_use_metiss_tome__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, _) = vmorph.use_metiss_tome()
        self.assertIs(is_success, True)
        (is_success, actual) = vmorph.use_metiss_tome()
        self.assertIs(is_success, False)
        expected = (4, "Lord")
        self.assertTupleEqual(actual, expected)
        expected = [
            ("use_metiss_tome", {}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)


class TraineeUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "TraineeUnit"
        kwargs = {'game_no': 8, "name": "Ross"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_promote__invalid_promotion(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, _) = vmorph.level_up(num_levels=9)
        self.assertIs(is_success, True)
        (is_success, actual) = vmorph.promote(promo_cls="")
        expected = [
            (10, "Fighter"),
            (10, "Pirate"),
            (10, "Journeyman (2)"),
        ]
        self.assertListEqual(actual, expected)
        actual = vmorph.history
        expected = [
            ("level_up", {'num_levels': 9}),
        ]
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_promote__level_too_low(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        vmorph.morph._set_max_level()
        (is_success, actual) = vmorph.promote(promo_cls="Pirate")
        self.assertIs(is_success, False)
        expected = [
            (10, "Pirate"),
        ]
        self.assertEqual(actual, expected)
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)

class TelliusKnightUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "TelliusKnightUnit"
        kwargs = {'game_no': 9, "name": "Kieran"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_init(self):
        """
        """
        vmorph = self.vmorph
        with patch("aenir.morph.Morph9") as MOCK_get_morph:
            vmorph.init()
        MOCK_get_morph.assert_called_once_with("Kieran")

    def test_equip_band(self):
        """
        """
        band_name = "Sword Band"
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_band(band_name=band_name)
        self.assertIs(is_success, True)
        self.assertIsNone(actual)
        # check history
        expected = [
            ("equip_band", {"band_name": "Sword Band"}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        # refetch
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        vmorph2.init()
        (is_success, actual) = vmorph2.equip_band(band_name=band_name)
        expected = {
            "Sword Band": False,
            "Soldier Band": True,
            "Fighter Band": True,
            "Archer Band": True,
            "Knight Band": True,
            "Paladin Band": True,
            "Pegasus Band": True,
            "Wyvern Band": True,
            "Mage Band": True,
            "Priest Band": True,
            "Thief Band": True,
        }
        self.assertDictEqual(actual, expected)

    def test_unequip_band(self):
        """
        """
        band_name = "Sword Band"
        vmorph = self.vmorph
        vmorph.init()
        vmorph.equip_band(band_name=band_name)
        #self.assertIs(is_success, True)
        (is_success, actual) = vmorph.unequip_band(band_name=band_name)
        self.assertIs(is_success, True)
        self.assertIsNone(actual)
        expected = [
            ("equip_band", {"band_name": band_name}),
            ("unequip_band", {"band_name": band_name}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        vmorph2.init()
        expected = [
            ["equip_band", {"band_name": "Sword Band"}],
            ["unequip_band", {"band_name": "Sword Band"}],
        ]
        actual = vmorph2.history
        self.assertListEqual(actual, expected)

    def test_equip_band__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_band(band_name="")
        expected = {
            "Sword Band": True,
            "Soldier Band": True,
            "Fighter Band": True,
            "Archer Band": True,
            "Knight Band": True,
            "Paladin Band": True,
            "Pegasus Band": True,
            "Wyvern Band": True,
            "Mage Band": True,
            "Priest Band": True,
            "Thief Band": True,
        }
        self.assertDictEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_unequip_band__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.unequip_band(band_name="")
        expected = {
            "Sword Band": False,
            "Soldier Band": False,
            "Fighter Band": False,
            "Archer Band": False,
            "Knight Band": False,
            "Paladin Band": False,
            "Pegasus Band": False,
            "Wyvern Band": False,
            "Mage Band": False,
            "Priest Band": False,
            "Thief Band": False,
        }
        self.assertDictEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_equip_knight_ward__no_inventory_space(self):
        """
        """
        vmorph = self.vmorph
        morph = vmorph.init()
        for band in morph.band_dict:
            morph.equipped_bands[band] = None
            if len(morph.equipped_bands) == 8:
                break
        (is_success, actual) = vmorph.equip_knight_ward()
        expected = {
            "Sword Band": True,
            "Soldier Band": True,
            "Fighter Band": True,
            "Archer Band": True,
            "Knight Band": True,
            "Paladin Band": True,
            "Pegasus Band": True,
            "Wyvern Band": True,
            "Mage Band": False,
            "Priest Band": False,
            "Thief Band": False,
        }
        self.assertDictEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_equip_knight_ward(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_knight_ward()
        self.assertIsNone(actual)
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        morph = vmorph2.init()
        with self.assertRaises(KnightWardError):
            morph.equip_knight_ward()
        expected = [
            ("equip_knight_ward", {}),
        ]
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, True)

    def test_unequip_knight_ward(self):
        """
        """
        vmorph = self.vmorph
        morph = vmorph.init()
        morph.equip_band("Sword Band")
        (is_success, actual) = vmorph.unequip_knight_ward()
        expected = {
            "Sword Band": True,
            "Soldier Band": False,
            "Fighter Band": False,
            "Archer Band": False,
            "Knight Band": False,
            "Paladin Band": False,
            "Pegasus Band": False,
            "Wyvern Band": False,
            "Mage Band": False,
            "Priest Band": False,
            "Thief Band": False,
        }
        self.assertEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

class TelliusNonKnightUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "TelliusNonKnightUnit"
        kwargs = {'game_no': 9, "name": "Ike"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_equip_knight_ward__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_knight_ward()
        expected = (
            'Titania',
            'Oscar',
            'Gatrie',
            'Kieran',
            'Brom',
            'Nephenee',
            'Astrid',
            'Makalov',
            'Devdan',
            'Tauroneo',
            'Geoffrey',
        )
        self.assertTupleEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

    def test_unequip_knight_ward__get_bounds(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        (is_success, actual) = vmorph.equip_knight_ward()
        expected = (
            'Titania',
            'Oscar',
            'Gatrie',
            'Kieran',
            'Brom',
            'Nephenee',
            'Astrid',
            'Makalov',
            'Devdan',
            'Tauroneo',
            'Geoffrey',
        )
        self.assertTupleEqual(actual, expected)
        expected = []
        actual = vmorph.history
        self.assertListEqual(actual, expected)
        self.assertIs(is_success, False)

class Lara(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "Lara"
        kwargs = {'game_no': 5, "name": "Lara"}
        self.vmorph = VirtualMorph.objects.create(morph_id=morph_id, **kwargs)

    def test_promote__get_bounds__short_route(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        vmorph.morph._set_max_level()
        (is_success, actual) = vmorph.promote()
        self.assertIs(is_success, False)
        expected = [
            (10, "Thief Fighter"),
            (1, "Dancer"),
        ]
        self.assertListEqual(actual, expected)
        (is_success, actual) = vmorph.promote(promo_cls="Dancer")
        self.assertIs(is_success, True)
        expected = [
            (1, "Dancer"),
        ]
        self.assertListEqual(actual, expected)
        logger.debug("Lara is now a Dancer.")
        vmorph.level_up(num_levels=9)
        (is_success, actual) = vmorph.promote()
        self.assertIs(is_success, True)
        expected = [
            (10, "Thief Fighter"),
        ]
        self.assertListEqual(actual, expected)
        logger.debug("Lara is now a Thief Fighter.")

    def test_promote__get_bounds__long_route(self):
        """
        """
        vmorph = self.vmorph
        vmorph.init()
        vmorph.morph._set_max_level()
        vmorph.level_up(num_levels=10)
        (is_success, actual) = vmorph.promote()
        self.assertIs(is_success, False)
        expected = [
            (10, "Thief Fighter"),
            (1, "Dancer"),
        ]
        self.assertListEqual(actual, expected)
        (is_success, actual) = vmorph.promote(promo_cls="Thief Fighter")
        self.assertIs(is_success, True)
        logger.debug("Lara is now a Thief Fighter.")
        expected = [
            (10, "Thief Fighter"),
        ]
        self.assertListEqual(actual, expected)
        (is_success, actual) = vmorph.promote()
        self.assertIs(is_success, True)
        expected = [
            (1, "Dancer"),
        ]
        self.assertListEqual(actual, expected)
        logger.debug("Lara is now a Dancer.")
        vmorph.level_up(num_levels=10)
        (is_success, actual) = vmorph.promote()
        self.assertIs(is_success, True)
        expected = [
            (10, "Thief Fighter"),
        ]
        self.assertListEqual(actual, expected)
        logger.debug("Lara is now a Thief Fighter.")

