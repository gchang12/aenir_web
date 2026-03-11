"""
"""

import uuid
import unittest
from unittest.mock import patch

from django.test import TestCase

from dracogate._logging import logger
from dracogate.models import VirtualMorph

URL_ENCODED_SOLIDUS = "%2F"

RESOURCE_URL = "/dracogate/api/morphs/"

class NormalUnit(TestCase):
    """
    FE6 Roy
    """

    def setUp(self):
        """
        FE6 Roy
        """
        logger.debug("%s", self.id())
        game_no = 6
        name = "Roy"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        kwargs['morph_id'] = "NormalUnit"
        self.kwargs = kwargs

    def test_list__verify_that_invalid_options_are_ignored(self):
        """
        FE6 Roy
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"invalid": "option"})
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data['preview'].keys())
        self.assertSetEqual(actual, expected)

    def test_list__verify_success(self):
        """
        FE6 Roy
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data['preview'].keys())
        self.assertSetEqual(actual, expected)
        actual = response.data['preview']
        expected = {
            "unitClass": "Lord",
            "level": (1, 20),
            "stats": [
                ("HP", 18.0, 60.0, 80),
                ("Pow", 5.0, 20.0, 30),
                ("Skl", 5.0, 20.0, 30),
                ("Spd", 7.0, 20.0, 30),
                ("Lck", 7.0, 30.0, 30),
                ("Def", 5.0, 20.0, 30),
                ("Res", 0.0, 20.0, 30),
                ("Con", 6.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_create(self):
        """
        FE6 Roy
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.post(url, data=kwargs)
        # check status code
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check pk value
        actual = response.data.pop('pk')
        logger.debug("Got a 'pk' value from the response: (%r, %r)", actual, type(actual))
        expected = VirtualMorph.objects.get().id
        self.assertEqual(actual, expected)

    def test_create__invalid_morph_id(self):
        """
        FE6 Roy
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs['morph_id'] = ""
        response = self.client.post(url, data=kwargs)
        # check status code
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check error code.
        actual = response.data['detail'].code
        expected = "INVALID_MORPH_ID"
        self.assertEqual(actual, expected)
        # check database.
        actual = VirtualMorph.objects.exists()
        expected = False
        self.assertIs(actual, expected)

class FatheredUnit(TestCase):
    """
    FE4 Lex!Lakche
    """

    def setUp(self):
        """
        FE4 Lex!Lakche
        """
        logger.debug("%s", self.id())
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE4 Lex!Lakche
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Swordfighter",
            "level": (1, 20),
            "stats": [
                ("HP", 30.0, 80.0, 80),
                ("Str", 10.0, 22.0, 30),
                ("Mag", 0.0, 15.0, 30),
                ("Skl", 13.0, 25.0, 30),
                ("Spd", 13.0, 25.0, 30),
                ("Lck", 8.0, 30.0, 30),
                ("Def", 7.0, 20.0, 30),
                ("Res", 0.0, 15.0, 30),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success_alt(self):
        """
        FE4 Lex!Lakche
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"father": "Claude"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Swordfighter",
            "level": (1, 20),
            "stats": [
                ("HP", 29.0, 80.0, 80),
                ("Str", 9.0, 22.0, 30),
                ("Mag", 1.0, 15.0, 30),
                ("Skl", 13.0, 25.0, 30),
                ("Spd", 13.0, 25.0, 30),
                ("Lck", 9.0, 30.0, 30),
                ("Def", 6.0, 20.0, 30),
                ("Res", 1.0, 15.0, 30),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_error(self):
        """
        FE4 Lex!Lakche
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("father")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data["missingParams"])
        expected = {"father"}
        self.assertSetEqual(actual, expected)
        actual = response.data["missingParams"]["father"]
        expected = (
            "Arden",
            "Azel",
            "Alec",
            "Claude",
            "Jamka",
            "Dew",
            "Noish",
            "Fin",
            "Beowolf",
            "Holyn",
            "Midayle",
            "Levin",
            "Lex",
        )
        self.assertTupleEqual(actual, expected)

    def test_create__bastard(self):
        """
        FE4 Lex!Lakche
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("father")
        kwargs['morph_id'] = "FatheredUnit"
        response = self.client.post(url, data=kwargs)
        # check status code
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # check error code
        actual = response.data['detail'].code
        expected = "UNIT_DNE"
        self.assertEqual(actual, expected)
        # check database.
        actual = VirtualMorph.objects.exists()
        expected = False
        self.assertIs(actual, expected)

class HardModeUnit(TestCase):
    """
    FE6 HM!Rutger
    """

    def setUp(self):
        """
        FE6 HM!Rutger
        """
        logger.debug("%s", self.id())
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": "false"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE6 HM!Rutger
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Myrmidon",
            "level": (4, 20),
            "stats": [
                ("HP", 22.0, 60.0, 80),
                ("Pow", 7.0, 20.0, 30),
                ("Skl", 12.0, 20.0, 30),
                ("Spd", 13.0, 20.0, 30),
                ("Lck", 2.0, 30.0, 30),
                ("Def", 5.0, 20.0, 30),
                ("Res", 0.0, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success_alt(self):
        """
        FE6 HM!Rutger
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({'hard_mode': 'true'})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Myrmidon",
            "level": (4, 20),
            "stats": [
                ("HP", 25.5, 60.0, 80),
                ("Pow", 8.75, 20.0, 30),
                ("Skl", 14.0, 20.0, 30),
                ("Spd", 15.0, 20.0, 30),
                ("Lck", 3.5, 30.0, 30),
                ("Def", 5.75, 20.0, 30),
                ("Res", 0.85, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_error(self):
        """
        FE6 HM!Rutger
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("hard_mode")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"hard_mode"}
        self.assertSetEqual(actual, expected)
        actual = response.data["missingParams"]["hard_mode"]
        expected = (False, True)
        self.assertTupleEqual(actual, expected)

    def test_create__validate_options(self):
        """
        FE6 HM!Rutger
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        # pre request-send check
        actual = kwargs['hard_mode']
        expected = "false"
        self.assertEqual(actual, expected)
        # send response
        kwargs["morph_id"] = "HARD_MODE_UNIT"
        response = self.client.post(url, data=kwargs)
        # check status code
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check option values
        pk = response.data.pop('pk')
        vmorph = VirtualMorph.objects.get(id=pk)
        actual = vmorph.options['hard_mode']
        expected = False
        self.assertIs(actual, expected)

class DeclinableUnit(TestCase):
    """
    FE6 Hugh
    """

    def setUp(self):
        """
        FE6 Hugh
        """
        logger.debug("%s", self.id())
        game_no = 6
        name = "Hugh"
        options = {"number_of_declines": 0}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE6 Hugh
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Mage",
            "level": (15, 20),
            "stats": [
                ("HP", 26.0, 60.0, 80),
                ("Pow", 13.0, 20.0, 30),
                ("Skl", 11.0, 20.0, 30),
                ("Spd", 12.0, 20.0, 30),
                ("Lck", 10.0, 30.0, 30),
                ("Def", 9.0, 20.0, 30),
                ("Res", 9.0, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success_alt1(self):
        """
        FE6 Hugh
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"number_of_declines": 1})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Mage",
            "level": (15, 20),
            "stats": [
                ("HP", 25.0, 60.0, 80),
                ("Pow", 12.0, 20.0, 30),
                ("Skl", 10.0, 20.0, 30),
                ("Spd", 11.0, 20.0, 30),
                ("Lck", 9.0, 30.0, 30),
                ("Def", 8.0, 20.0, 30),
                ("Res", 8.0, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success_alt2(self):
        """
        FE6 Hugh
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"number_of_declines": 2})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Mage",
            "level": (15, 20),
            "stats": [
                ("HP", 24.0, 60.0, 80),
                ("Pow", 11.0, 20.0, 30),
                ("Skl", 9.0, 20.0, 30),
                ("Spd", 10.0, 20.0, 30),
                ("Lck", 8.0, 30.0, 30),
                ("Def", 7.0, 20.0, 30),
                ("Res", 7.0, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success_alt3(self):
        """
        FE6 Hugh
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"number_of_declines": 3})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Mage",
            "level": (15, 20),
            "stats": [
                ("HP", 23.0, 60.0, 80),
                ("Pow", 10.0, 20.0, 30),
                ("Skl", 8.0, 20.0, 30),
                ("Spd", 9.0, 20.0, 30),
                ("Lck", 7.0, 30.0, 30),
                ("Def", 6.0, 20.0, 30),
                ("Res", 6.0, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_error(self):
        """
        FE6 Hugh
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("number_of_declines")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"number_of_declines"}
        self.assertSetEqual(actual, expected)
        actual = response.data["missingParams"]["number_of_declines"]
        expected = (0, 1, 2, 3)
        self.assertTupleEqual(actual, expected)

    def test_list__verify_invalid_values(self):
        """
        FE6 Hugh
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs["number_of_declines"] = 4
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"number_of_declines"}
        self.assertSetEqual(actual, expected)

class Gonzales(TestCase):
    """
    FE6 Gonzales
    """

    def setUp(self):
        """
        FE6 Gonzales
        """
        logger.debug("%s", self.id())
        game_no = 6
        name = "Gonzales"
        options = {"hard_mode": "false", "chapter": "10A"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE6 Gonzales
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Bandit",
            "level": (5, 20),
            "stats": [
                ("HP", 36.0, 60.0, 80),
                ("Pow", 12.0, 20.0, 30),
                ("Skl", 5.0, 20.0, 30),
                ("Spd", 9.0, 20.0, 30),
                ("Lck", 5.0, 30.0, 30),
                ("Def", 6.0, 20.0, 30),
                ("Res", 0.0, 20.0, 30),
                ("Con", 15.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success__elphin_no_hm(self):
        """
        FE6 Gonzales
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"hard_mode": "false", "chapter": "10B"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Bandit",
            "level": (11, 20),
            "stats": [
                ("HP", 36.0, 60.0, 80),
                ("Pow", 12.0, 20.0, 30),
                ("Skl", 5.0, 20.0, 30),
                ("Spd", 9.0, 20.0, 30),
                ("Lck", 5.0, 30.0, 30),
                ("Def", 6.0, 20.0, 30),
                ("Res", 0.0, 20.0, 30),
                ("Con", 15.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success__lalum_hm(self):
        """
        FE6 Gonzales
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"hard_mode": "true"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Bandit",
            "level": (5, 20),
            "stats": [
                ("HP", 42.56, 60.0, 80),
                ("Pow", 16.0, 20.0, 30),
                ("Skl", 7.4, 20.0, 30),
                ("Spd", 10.6, 20.0, 30),
                ("Lck", 6.2, 30.0, 30),
                ("Def", 6.8, 20.0, 30),
                ("Res", 0.8, 20.0, 30),
                ("Con", 15.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success__elphin_hm(self):
        """
        FE6 Gonzales
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"hard_mode": "true", "chapter": "10B"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Bandit",
            "level": (11, 20),
            "stats": [
                ("HP", 42.56, 60.0, 80),
                ("Pow", 16.0, 20.0, 30),
                ("Skl", 7.4, 20.0, 30),
                ("Spd", 10.6, 20.0, 30),
                ("Lck", 6.2, 30.0, 30),
                ("Def", 6.8, 20.0, 30),
                ("Res", 0.8, 20.0, 30),
                ("Con", 15.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_error1(self):
        """
        FE6 Gonzales
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("chapter")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"chapter"}
        self.assertSetEqual(actual, expected)
        actual = response.data['missingParams']["chapter"]
        expected = ("10A", "10B")
        self.assertTupleEqual(actual, expected)

    def test_list__verify_error2(self):
        """
        FE6 Gonzales
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("hard_mode")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"hard_mode"}
        self.assertSetEqual(actual, expected)
        actual = response.data['missingParams']["hard_mode"]
        expected = (False, True)
        self.assertTupleEqual(actual, expected)

class LyndisLeague(TestCase):
    """
    FE7 (No-LynMode)!Lyn
    """

    def setUp(self):
        """
        FE7 (No-LynMode)!Lyn
        """
        logger.debug("%s", self.id())
        game_no = 7
        name = "Lyn"
        options = {"lyn_mode": "false"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_error(self):
        """
        FE7 (No-LynMode)!Lyn
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("lyn_mode")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data["missingParams"])
        expected = {"lyn_mode"}
        self.assertSetEqual(actual, expected)
        actual = response.data["missingParams"]["lyn_mode"]
        expected = (False, True)
        self.assertTupleEqual(actual, expected)

    def test_list__verify_success__lyn_mode(self):
        """
        FE7 (No-LynMode)!Lyn
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Lord",
            "level": (1, 20),
            "stats": [
                ("HP", 16.0, 60.0, 80),
                ("Pow", 4.0, 20.0, 30),
                ("Skl", 7.0, 20.0, 30),
                ("Spd", 9.0, 20.0, 30),
                ("Lck", 5.0, 30.0, 30),
                ("Def", 2.0, 20.0, 30),
                ("Res", 0.0, 20.0, 30),
                ("Con", 5.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success__no_lyn_mode(self):
        """
        FE7 (No-LynMode)!Lyn
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Lord",
            "level": (4, 20),
            "stats": [
                ("HP", 18.0, 60.0, 80),
                ("Pow", 5.0, 20.0, 30),
                ("Skl", 10.0, 20.0, 30),
                ("Spd", 11.0, 20.0, 30),
                ("Lck", 5.0, 30.0, 30),
                ("Def", 2.0, 20.0, 30),
                ("Res", 0.0, 20.0, 30),
                ("Con", 5.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

class Ninian(TestCase):
    """
    FE7 Ninian
    """

    def setUp(self):
        """
        FE7 Ninian
        """
        logger.debug("%s", self.id())
        game_no = 7
        name = "Ninian"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE7 Ninian
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)

    def test_list__verify_server_failure(self):
        """
        FE7 Ninian
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        detail = response.data['detail']
        #self.assertIn("code", detail)
        self.assertEqual(detail.code, "UNIT_DNE")

class Nils(TestCase):
    """
    FE7 Nils
    """

    def setUp(self):
        """
        FE7 Nils
        """
        logger.debug("%s", self.id())
        game_no = 7
        name = "Nils"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE7 Nils
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Bard",
            "level": (1, 20),
            "stats": [
                ("HP", 14.0, 60.0, 80),
                ("Pow", 0.0, 10.0, 30),
                ("Skl", 0.0, 10.0, 30),
                ("Spd", 12.0, 30.0, 30),
                ("Lck", 10.0, 30.0, 30),
                ("Def", 5.0, 24.0, 30),
                ("Res", 4.0, 26.0, 30),
                ("Con", 3.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success_alt(self):
        """
        FE7 Nils
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "false"})
        response = self.client.get(url, data=kwargs)
        actual = response.data['preview']
        expected = {
            "unitClass": "Bard",
            "level": (1, 20),
            "stats": [
                ("HP", 14.0, 60.0, 80),
                ("Pow", 0.0, 10.0, 30),
                ("Skl", 0.0, 10.0, 30),
                ("Spd", 12.0, 30.0, 30),
                ("Lck", 10.0, 30.0, 30),
                ("Def", 5.0, 24.0, 30),
                ("Res", 4.0, 26.0, 30),
                ("Con", 3.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

class BonusUnit(TestCase):
    """
    FE8 Lyon
    """

    def setUp(self):
        """
        FE8 Lyon
        """
        logger.debug("%s", self.id())
        game_no = 8
        name = "Lyon"
        options = {}
        kwargs = {"game_no": game_no, "name": name, "morph_id": "BonusUnit"}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        FE8 Lyon
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, query_params=kwargs)
        self.assertNotIn("missingParams", response.data)

class InvalidGame(TestCase):
    """
    FE10 Ike
    """

    def setUp(self):
        """
        FE10 Ike
        """
        logger.debug("%s", self.id())
        game_no = 10
        name = "Ike"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_error(self):
        """
        FE10 Ike
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        # verify status code
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # verify response data fields
        actual = set(response.data.keys())
        expected = {"detail"}
        self.assertSetEqual(actual, expected)
        # verify response data values
        detail = response.data["detail"]
        actual = detail.code
        expected = "INVALID_GAME"
        self.assertEqual(actual, expected)

    def test_create__unit_from_invalid_game(self):
        """
        FE10 Ike
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs['morph_id'] = "InvalidGame"
        response = self.client.post(url, data=kwargs)
        # check status code
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # check error code
        actual = response.data['detail'].code
        expected = "INVALID_GAME"
        self.assertEqual(actual, expected)
        # check database.
        actual = VirtualMorph.objects.exists()
        expected = False
        self.assertIs(actual, expected)

class InvalidUnit(TestCase):
    """
    FE7 Marth (?)
    """

    def setUp(self):
        """
        FE7 Marth (?)
        """
        logger.debug("%s", self.id())
        game_no = 7
        name = "Marth"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_error(self):
        """
        FE7 Marth (?)
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        # verify status code
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # verify response data fields
        expected = {"detail"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)
        # verify response data values
        detail = response.data["detail"]
        # 1
        actual = detail.code
        expected = "UNIT_DNE"
        self.assertEqual(actual, expected)
        # 2
        #actual = detail['code']
        #expected = "UNIT_DNE"
        #self.assertEqual(actual, expected)

    def test_create__invalid_unit(self):
        """
        FE7 Marth (?)
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs['morph_id'] = "InvalidUnit"
        response = self.client.post(url, data=kwargs)
        # check status code
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # check error code
        actual = response.data['detail'].code
        expected = "UNIT_DNE"
        self.assertEqual(actual, expected)
        # check database.
        actual = VirtualMorph.objects.exists()
        expected = False
        self.assertIs(actual, expected)


class FE4UnitForSimulatingInvalidOperations(TestCase):
    """
    FE4 Sigurd
    """

    def setUp(self):
        """
        FE4 Sigurd
        """
        logger.debug("%s", self.id())
        morph_id = "FE4!Sigurd"
        game_no = 4
        name = "Sigurd"
        options = {}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_invalid_morph_method(self):
        """
        FE4 Sigurd
        """
        method_name = ""
        num_levels = 16
        data = {
            "num_levels": num_levels,
        }
        expected_error_code = "BAD_MORPH_METHOD"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # check database
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check offline data
        morph = self.vmorph.init()
        actual = morph.current_lv
        expected = 5
        self.assertEqual(actual, expected)

    def test_use_stat_booster(self):
        """
        FE4 Sigurd
        """
        method_name = "use_stat_booster"
        data = {
            "item_name": "Angelic Robe"
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_use_afas_drops(self):
        """
        FE4 Sigurd
        """
        method_name = "use_afas_drops"
        data = {}
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_use_metiss_tome(self):
        """
        FE4 Sigurd
        """
        method_name = "use_metiss_tome"
        data = {}
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_equip_band(self):
        """
        FE4 Sigurd
        """
        method_name = "equip_band"
        data = {
            "band_name": "Sword Band"
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_unequip_band(self):
        """
        FE4 Sigurd
        """
        method_name = "unequip_band"
        data = {
            "band_name": "Sword Band"
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_equip_scroll(self):
        """
        FE4 Sigurd
        """
        method_name = "equip_scroll"
        data = {
            "scroll_name": "Odo"
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_unequip_scroll(self):
        """
        FE4 Sigurd
        """
        method_name = "unequip_scroll"
        data = {
            "scroll_name": "Odo"
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        expected = expected_error_code
        actual = response.data['detail'].code
        self.assertEqual(actual, expected)

    def test_level_up__30(self):
        """
        FE4 Sigurd
        """
        method_name = "level_up"
        data = {
            "num_levels": 25,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["level_up", {'num_levels': 25}],
        ]
        self.assertListEqual(actual, expected)
        morph = self.vmorph.init()

class FE6Unit(TestCase):
    """
    FE6 (HardMode)!Rutger
    """

    def setUp(self):
        """
        FE6 (HardMode)!Rutger
        """
        logger.debug("%s", self.id())
        morph_id = "FE6!Rutger"
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": True}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        vmorph.init()
        vmorph.morph._set_max_level()
        self.vmorph = vmorph

    def test_retrieve(self):
        """
        FE6 (HardMode)!Rutger
        """
        # set up session['morphs']
        #session = self.client.session
        #session['morphs'] = [self.vmorph.id]
        #session.save()
        # usual
        url = RESOURCE_URL + str(self.vmorph.id) + "/"
        logger.debug("Sending GET request to: %s", url)
        response = self.client.get(url)
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        logger.debug("response.data: %r", response.data)

    def test_retrieve__fail(self):
        """
        FE6 (HardMode)!Rutger
        """
        # set up session['morphs']
        #session = self.client.session
        #session['morphs'] = [self.vmorph.id]
        #session.save()
        # first, confirm that vmorph.id does not exist.
        wmorph_id = uuid.uuid4()
        actual = VirtualMorph.objects.filter(id=wmorph_id).exists()
        expected = False
        self.assertIs(actual, expected)
        # send request to fetch nonexistent data.
        url = RESOURCE_URL + str(wmorph_id) + "/"
        response = self.client.get(url)
        # check status
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data['detail'].code
        expected = "not_found"
        self.assertEqual(actual, expected)

    def test_destroy(self):
        """
        FE6 (HardMode)!Rutger
        """
        url = RESOURCE_URL + str(self.vmorph.id) + "/"
        response = self.client.delete(url)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data
        #expected = {}
        #self.assertDictEqual(actual, expected)
        self.assertIsNone(actual)
        # check database
        actual = VirtualMorph.objects.filter(id=self.vmorph.id).exists()
        expected = False
        self.assertIs(actual, expected)

    def test_destroy__fail(self):
        """
        FE6 (HardMode)!Rutger
        """
        # first, confirm that vmorph.id does not exist.
        wmorph_id = uuid.uuid4()
        actual = VirtualMorph.objects.filter(id=wmorph_id).exists()
        expected = False
        self.assertIs(actual, expected)
        # send request to delete nonexistent data.
        url = RESOURCE_URL + str(wmorph_id) + "/"
        response = self.client.delete(url)
        # check status
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data['detail'].code
        expected = "VIRTUALMORPH_NOT_FOUND"
        self.assertEqual(actual, expected)

    def test_level_up__no_rehearsal(self):
        """
        FE6 (HardMode)!Rutger
        """
        method_name = "level_up"
        num_levels = 16
        data = {
            "num_levels": num_levels,
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            "morph": {
                'unitClass': "Myrmidon",
                'level': (20, 20),
                'stats': [
                    ("HP", 38.3, 60.0, 80.0),
                    ("Pow", 13.55, 20.0, 30.0),
                    ("Skl", 20.0, 20.0, 30.0),
                    ("Spd", 20.0, 20.0, 30.0),
                    ("Lck", 8.3, 30.0, 30.0),
                    ("Def", 8.95, 20.0, 30.0),
                    ("Res", 4.05, 20.0, 30.0),
                    ("Con", 7.0, 20.0, 25.0),
                    ("Mov", 5.0, 15.0, 15.0),
                ],
            },
        }
        self.assertDictEqual(actual, expected)
        # check database
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["level_up", {"num_levels": 16}],
        ]
        self.assertListEqual(actual, expected)

    def test_level_up__rehearsal(self):
        """
        FE6 (HardMode)!Rutger
        """
        method_name = "level_up"
        num_levels = 16
        data = {
            "num_levels": num_levels,
        }
        expected_error_code = "METHOD_NOT_DEFINED_ON_MORPH"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            "morph": {
                'unitClass': "Myrmidon",
                'level': (20, 20),
                'stats': [
                    ("HP", 38.3, 60.0, 80.0),
                    ("Pow", 13.55, 20.0, 30.0),
                    ("Skl", 20.0, 20.0, 30.0),
                    ("Spd", 20.0, 20.0, 30.0),
                    ("Lck", 8.3, 30.0, 30.0),
                    ("Def", 8.95, 20.0, 30.0),
                    ("Res", 4.05, 20.0, 30.0),
                    ("Con", 7.0, 20.0, 25.0),
                    ("Mov", 5.0, 15.0, 15.0),
                ],
            },
            "paramBounds": (5, 20),
        }
        self.assertDictEqual(actual, expected)
        # check database
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check offline data
        morph = self.vmorph.morph
        actual = morph.current_lv
        expected = 4
        self.assertEqual(actual, expected)

    def test_level_up__invalid_args(self):
        """
        FE6 (HardMode)!Rutger
        """
        method_name = "level_up"
        num_levels = 16
        data = {
            "numLevels": num_levels,
        }
        expected_error_code = "required"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data['num_levels'][0].code
        expected = expected_error_code
        self.assertEqual(actual, expected)
        # check database
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check offline data
        morph = self.vmorph.morph
        actual = morph.current_lv
        expected = 4
        self.assertEqual(actual, expected)

    def test_level_up__morph_err(self):
        """
        FE6 (HardMode)!Rutger
        """
        method_name = "level_up"
        num_levels = 17
        data = {
            "num_levels": num_levels,
        }
        expected_error_code = "UNABLE_TO_UPDATE"
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data['detail'].code
        expected = expected_error_code
        self.assertEqual(actual, expected)
        # check database
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check offline data
        morph = self.vmorph.morph
        actual = morph.current_lv
        expected = 4
        self.assertEqual(actual, expected)

class FE7Unit(TestCase):
    """
    FE7 (LynMode)!Lyn
    """

    def setUp(self):
        """
        FE7 (LynMode)!Lyn
        """
        logger.debug("%s", self.id())
        morph_id = "FE7!Lyn"
        game_no = 7
        name = "Lyn"
        options = {"lyn_mode": True}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_promote__morph_err(self):
        """
        FE7 (LynMode)!Lyn
        """
        method_name = "promote"
        promo_cls = "Blade Lord"
        data = {
            "promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.init().current_lv
        expected = 1
        self.assertEqual(actual, expected)
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check response
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        actual = response.data
        expected = {
            'morph': {
                'level': (1, 20),
                'unitClass': 'Blade Lord',
                'stats': [
                    ('HP', 32.3, 60.0, 80.0),
                    ('Pow', 13.6, 24.0, 30.0),
                    ('Skl', 20.4, 29.0, 30.0),
                    ('Spd', 20.0, 30.0, 30.0),
                    ('Lck', 15.45, 30.0, 30.0),
                    ('Def', 8.8, 22.0, 30.0),
                    ('Res', 10.7, 22.0, 30.0),
                    ('Con', 6.0, 25.0, 25.0),
                    ('Mov', 6.0, 15.0, 15.0)
                ],
            },
            "paramBounds": [(10, "Blade Lord")],
        }
        self.assertDictEqual(actual, expected)

    def test_use_stat_booster(self):
        """
        FE7 (LynMode)!Lyn
        """
        method_name = "use_stat_booster"
        data = {
            "item_name": "Angelic Robe"
        }
        boosted_hp = (self.vmorph.init().current_stats.HP / 100) + 7.0
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check offline data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["use_stat_booster", {'item_name': "Angelic Robe"}],
        ]
        self.assertListEqual(actual, expected)
        # check response
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check numerical stats data
        morph = vmorph.init()
        actual = response.data
        expected = {
            "morph": {
                "unitClass": "Lord",
                'level': (1, 20),
                'stats': [
                    ("HP", boosted_hp, 60.0, 80.0),
                    ("Pow", 4.0, 20.0, 30.0),
                    ("Skl", 7.0, 20.0, 30.0),
                    ("Spd", 9.0, 20.0, 30.0),
                    ("Lck", 5.0, 30.0, 30.0),
                    ("Def", 2.0, 20.0, 30.0),
                    ("Res", 0.0, 20.0, 30.0),
                    ("Con", 5.0, 20.0, 25.0),
                    ("Mov", 5.0, 15.0, 15.0),
                ],
            },
            #"paramBounds": None,
        }
        self.assertDictEqual(actual, expected)

class FE7PromotionReadyUnit(TestCase):
    """
    FE7 (HardMode)!Legault
    """

    def setUp(self):
        """
        FE7 (HardMode)!Legault
        """
        logger.debug("%s", self.id())
        morph_id = "FE7!Legault"
        game_no = 7
        name = "Legault"
        options = {"hard_mode": True}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_promote__rehearsal(self):
        """
        FE7 (HardMode)!Legault
        """
        method_name = "promote"
        promo_cls = "Assassin"
        data = {
            "promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            "morph": {
                'unitClass': "Assassin",
                'level': (1, 20),
                'stats': [
                    ("HP", 31.5, 60.0, 80.0),
                    ("Pow", 9.25, 20.0, 30.0),
                    ("Skl", 13.25, 30.0, 30.0),
                    ("Spd", 17.0, 30.0, 30.0),
                    ("Lck", 12.0, 30.0, 30.0),
                    ("Def", 10.25, 20.0, 30.0),
                    ("Res", 6.0, 20.0, 30.0),
                    ("Con", 9.0, 20.0, 25.0),
                    ("Mov", 6.0, 15.0, 15.0),
                ],
            },
            "paramBounds": [(10, "Assassin")],
        }
        self.assertDictEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        actual = vmorph.init().current_stats.as_dict()
        expected = {
            "HP": 28_50,
            "Pow": 8_25,
            "Skl": 13_25,
            "Spd": 17_00,
            "Lck": 12_00,
            "Def": 8_25,
            "Res": 4_00,
            "Con": 9_00,
            "Mov": 6_00,
        }
        self.assertDictEqual(actual, expected)
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)

    def test_promote__no_rehearsal(self):
        """
        FE7 (HardMode)!Legault
        """
        method_name = "promote"
        promo_cls = "Assassin"
        data = {
            "promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        morph = vmorph.init()
        actual = morph.current_lv
        expected = 1
        self.assertEqual(actual, expected)
        actual = vmorph.history
        expected = [
            ["promote", {"promo_cls": "Assassin"}],
        ]
        self.assertListEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            "morph": {
                'unitClass': "Assassin",
                'level': (1, 20),
                'stats': [
                    ("HP", 31.5, 60.0, 80.0),
                    ("Pow", 9.25, 20.0, 30.0),
                    ("Skl", 13.25, 30.0, 30.0),
                    ("Spd", 17.0, 30.0, 30.0),
                    ("Lck", 12.0, 30.0, 30.0),
                    ("Def", 10.25, 20.0, 30.0),
                    ("Res", 6.0, 20.0, 30.0),
                    ("Con", 9.0, 20.0, 25.0),
                    ("Mov", 6.0, 15.0, 15.0),
                ],
            },
            #"paramBounds": [(10, "Assassin")],
        }
        self.assertDictEqual(actual, expected)

    def test_use_afas_drops__no_rehearsal(self):
        """
        FE7 (HardMode)!Legault
        """
        method_name = "use_afas_drops"
        #promo_cls = "Assassin"
        data = {
            #"promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["use_afas_drops", {}],
        ]
        self.assertListEqual(actual, expected)
        morph = vmorph.init()
        expected = {
            "HP": 65,
            "Pow": 30,
            "Skl": 50,
            "Spd": 65,
            "Lck": 65,
            "Def": 30,
            "Res": 30,
            "Con": 0,
            "Mov": 0,
        }
        actual = morph.growth_rates.as_dict()
        self.assertDictEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            "morph": {
                "unitClass": "Thief",
                "level": (12, 20),
                'stats': [
                    ('HP', 60, 65),
                    ('Pow', 25, 30),
                    ('Skl', 45, 50),
                    ('Spd', 60, 65),
                    ('Lck', 60, 65),
                    ('Def', 25, 30),
                    ('Res', 25, 30),
                    ('Con', None, None),
                    ('Mov', None, None),
                ],
            },
            #"paramBounds": None,
        }
        self.assertDictEqual(actual, expected)

class FE6UnitPrePromote(TestCase):
    """
    FE6 Marcus
    """

    def setUp(self):
        """
        FE6 Marcus
        """
        logger.debug("%s", self.id())
        game_no = 6
        name = "Marcus"
        options = {}
        morph_id = "FE6UnitPrePromote"
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_promote__rehearsal__fail(self):
        """
        FE6 Marcus
        """
        method_name = "promote"
        promo_cls = "Paladin"
        data = {
            "promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        morph = vmorph.init()
        actual = morph.current_lv
        expected = 1
        self.assertEqual(actual, expected)
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            "morph": {
                "level": (20, 20),
                "unitClass": "Paladin",
                'stats': [
                    ('HP', 43.4, 60.0, 80.0),
                    ('Pow', 13.75, 25.0, 30.0),
                    ('Skl', 17.8, 28.0, 30.0),
                    ('Spd', 15.75, 25.0, 30.0),
                    ('Lck', 13.8, 30.0, 30.0),
                    ('Def', 11.85, 25.0, 30.0),
                    ('Res', 11.8, 25.0, 30.0),
                    ('Con', 11.0, 20.0, 25.0),
                    ('Mov', 8.0, 15.0, 15.0),
                ],
            },
            "paramBounds": None,
        }
        self.assertDictEqual(actual, expected)

class FE8UnitWithBranchedPromotion(TestCase):
    """
    FE8 Gerik
    """

    def setUp(self):
        """
        FE8 Gerik
        """
        logger.debug("%s", self.id())
        morph_id = "FE8!Gerik"
        game_no = 8
        name = "Gerik"
        options = {}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_promote__rehearsal__fail(self):
        """
        FE8 Gerik
        """
        method_name = "promote"
        promo_cls = "NotARealUnitClass"
        data = {
            "promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.get(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        morph = vmorph.init()
        actual = morph.current_lv
        expected = 10
        self.assertEqual(actual, expected)
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check response data
        actual = response.data
        expected = {
            'morph': {
                'level': (20, 20),
                'unitClass': 'Mercenary',
                'stats': [
                    ('HP', 41.0, 60.0, 80.0),
                    ('Pow', 18.5, 20.0, 30.0),
                    ('Skl', 17.0, 20.0, 30.0),
                    ('Spd', 16.0, 20.0, 30.0),
                    ('Lck', 11.0, 30.0, 30.0),
                    ('Def', 13.5, 20.0, 30.0),
                    ('Res', 6.5, 20.0, 30.0),
                    ('Con', 13.0, 20.0, 25.0),
                    ('Mov', 5.0, 15.0, 15.0)
                ],
            },
            "paramBounds": [
                (10, "Hero"),
                (10, "Ranger (M)"),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_promote__no_rehearsal__fail(self):
        """
        FE8 Gerik
        """
        method_name = "promote"
        promo_cls = "NotARealUnitClass"
        data = {
            "promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 400
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        morph = vmorph.init()
        actual = morph.current_lv
        expected = 10
        self.assertEqual(actual, expected)
        # check database
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = []
        self.assertListEqual(actual, expected)
        # check response data
        actual = response.data['detail'].code
        expected = "UNABLE_TO_UPDATE"
        self.assertEqual(actual, expected)

    def test_use_metiss_tome__no_rehearsal(self):
        """
        FE8 Gerik
        """
        method_name = "use_metiss_tome"
        #promo_cls = "Assassin"
        data = {
            #"promo_cls": promo_cls,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["use_metiss_tome", {}],
        ]
        self.assertListEqual(actual, expected)
        morph = vmorph.init()
        expected = {
            "HP": 95,
            "Pow": 50,
            "Skl": 45,
            "Spd": 35,
            "Lck": 35,
            "Def": 40,
            "Res": 30,
            "Con": 0,
            "Mov": 0,
        }
        actual = morph.growth_rates.as_dict()
        self.assertDictEqual(actual, expected)

class FE5Unit(TestCase):
    """
    FE5 Evayle
    """

    def setUp(self):
        """
        FE5 Evayle
        """
        logger.debug("%s", self.id())
        game_no = 5
        name = "Evayle"
        options = {}
        morph_id = "FE5Unit"
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_set_scrolls(self):
        """
        """
        method_name = "set_scrolls"
        scrolls = [
            'Baldo',
            'Blaggi',
            'Dain',
            'Fala',
        ]
        data = {"scrolls": scrolls}
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        #actual[0][1]['scrolls'] = set(actual[0][1]['scrolls'])
        expected = [
            ["set_scrolls", {"scrolls": scrolls}],
        ]
        self.assertListEqual(actual, expected)

    def test_equip_scroll__no_rehearsal(self):
        """
        FE5 Evayle
        """
        method_name = "equip_scroll"
        scroll_name = "Odo"
        data = {
            "scroll_name": scroll_name,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["equip_scroll", {"scroll_name": "Odo"}],
        ]
        self.assertListEqual(actual, expected)

    def test_unequip_scroll__no_rehearsal(self):
        """
        FE5 Evayle
        """
        method_name = "unequip_scroll"
        scroll_name = "Odo"
        data = {
            "scroll_name": scroll_name,
        }
        # set up
        self.vmorph.init()
        self.vmorph.equip_scroll(**data)
        self.vmorph.save()
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["equip_scroll", {"scroll_name": "Odo"}],
            ["unequip_scroll", {"scroll_name": "Odo"}],
        ]
        self.assertListEqual(actual, expected)

class FE9KnightUnit(TestCase):
    """
    FE9 Oscar
    """

    def setUp(self):
        """
        FE9 Oscar
        """
        logger.debug("%s", self.id())
        game_no = 9
        name = "Oscar"
        options = {}
        morph_id = "FE9KnightUnit"
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_equip_band__no_rehearsal(self):
        """
        FE9 Oscar
        """
        method_name = "equip_band"
        band_name = "Sword Band"
        data = {
            "band_name": band_name,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["equip_band", {"band_name": "Sword Band"}],
        ]
        self.assertListEqual(actual, expected)

    def test_unequip_band__no_rehearsal(self):
        """
        FE9 Oscar
        """
        method_name = "unequip_band"
        band_name = "Sword Band"
        data = {
            "band_name": band_name,
        }
        # set up
        self.vmorph.init()
        self.vmorph.equip_band(**data)
        self.vmorph.save()
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["equip_band", {"band_name": "Sword Band"}],
            ["unequip_band", {"band_name": "Sword Band"}],
        ]
        self.assertListEqual(actual, expected)

    def test_equip_knight_ward__no_rehearsal(self):
        """
        FE9 Oscar
        """
        method_name = "equip_knight_ward"
        #band_name = "Sword Band"
        data = {
            #"band_name": band_name,
        }
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["equip_knight_ward", {}],
        ]
        self.assertListEqual(actual, expected)

    def test_unequip_knight_ward__no_rehearsal(self):
        """
        FE9 Oscar
        """
        method_name = "unequip_knight_ward"
        #band_name = "Sword Band"
        data = {
            #"band_name": band_name,
        }
        # set up
        self.vmorph.init()
        self.vmorph.equip_knight_ward(**data)
        self.vmorph.save()
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        expected = [
            ["equip_knight_ward", {}],
            ["unequip_knight_ward", {}],
        ]
        self.assertListEqual(actual, expected)

    def test_set_bands(self):
        """
        """
        method_name = "set_bands"
        bands = [
            'Archer Band',
            'Fighter Band',
            'Soldier Band',
            'Sword Band',
        ]
        data = {"bands": bands}
        # usual stuff
        url = RESOURCE_URL + str(self.vmorph.id) + "/" + method_name +"/"
        response = self.client.patch(url, query_params=data)
        # check status
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        # check server-side data
        vmorph = VirtualMorph.objects.get()
        actual = vmorph.history
        #actual[0][1]['bands'] = set(actual[0][1]['bands'])
        expected = [
            ["set_bands", {"bands": bands}],
        ]
        self.assertListEqual(actual, expected)

