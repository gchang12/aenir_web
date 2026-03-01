"""
"""

import unittest
from unittest.mock import patch

from django.test import TestCase

from dracogate._logging import logger
from dracogate.models import VirtualMorph

URL_ENCODED_SOLIDUS = "%2F"

RESOURCE_URL = "/dracogate/api/morphs/"

class NormalUnit(TestCase):
    """
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"invalid": "option"})
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)

    def test_list__verify_success(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)
        actual = response.data
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
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"father": "Claude"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({'hard_mode': 'true'})
        response = self.client.get(url, data=kwargs)
        actual = response.data
        expected = {
            "unitClass": "Myrmidon",
            "level": (4, 20),
            "stats": [
                ("HP", 26.0, 60.0, 80),
                ("Pow", 9.0, 20.0, 30),
                ("Skl", 14.0, 20.0, 30),
                ("Spd", 15.0, 20.0, 30),
                ("Lck", 4.0, 30.0, 30),
                ("Def", 6.0, 20.0, 30),
                ("Res", 1.0, 20.0, 30),
                ("Con", 7.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_error(self):
        """
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
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"number_of_declines": 1})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"number_of_declines": 2})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"number_of_declines": 3})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        game_no = 6
        name = "Gonzales"
        options = {"hard_mode": "false", "route": "Lalum"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"hard_mode": "false", "route": "Elphin"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"hard_mode": "true"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
        expected = {
            "unitClass": "Bandit",
            "level": (5, 20),
            "stats": [
                ("HP", 43.0, 60.0, 80),
                ("Pow", 16.0, 20.0, 30),
                ("Skl", 7.0, 20.0, 30),
                ("Spd", 11.0, 20.0, 30),
                ("Lck", 6.0, 30.0, 30),
                ("Def", 7.0, 20.0, 30),
                ("Res", 1.0, 20.0, 30),
                ("Con", 15.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_success__elphin_hm(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"hard_mode": "true", "route": "Elphin"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
        expected = {
            "unitClass": "Bandit",
            "level": (11, 20),
            "stats": [
                ("HP", 43.0, 60.0, 80),
                ("Pow", 16.0, 20.0, 30),
                ("Skl", 7.0, 20.0, 30),
                ("Spd", 11.0, 20.0, 30),
                ("Lck", 6.0, 30.0, 30),
                ("Def", 7.0, 20.0, 30),
                ("Res", 1.0, 20.0, 30),
                ("Con", 15.0, 20.0, 25),
                ("Mov", 5.0, 15.0, 15),
            ],
        }
        self.assertDictEqual(actual, expected)

    def test_list__verify_error1(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.pop("route")
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"route"}
        self.assertSetEqual(actual, expected)
        actual = response.data['missingParams']["route"]
        expected = ("Lalum", "Elphin")
        self.assertTupleEqual(actual, expected)

    def test_list__verify_error2(self):
        """
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
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)

    def test_list__verify_server_failure(self):
        """
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
    """

    def setUp(self):
        """
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "false"})
        response = self.client.get(url, data=kwargs)
        actual = response.data
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
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        game_no = 8
        name = "Lyon"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_list__verify_success(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

class InvalidGame(TestCase):
    """
    """

    def setUp(self):
        """
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
    """

    def setUp(self):
        """
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


'''
create
- Does it really create a VirtualMorph object in the database?
- What happens if bad parameters are put in?
delete
- What happens if you try to delete some unit who exists?
- What happens if you try to delete some unit who doesn't exist?
partial_update
- Check that the record hasn't been updated.
- Have the parameter-bounds been returned?
Update
- Check that the record's been updated.
- Have the right values been returned?
'''

@unittest.skip("I was doing dumb stuff.")
class UnitWithSlashedMorphID(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "Na/me"
        game_no = 6
        name = "Marcus"
        options = {}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_retrieve__fail1(self):
        """
        """
        url = RESOURCE_URL + self.vmorph.morph_id + "/"
        response = self.client.get(url)
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)

    def test_retrieve__fail2(self):
        """
        """
        url = RESOURCE_URL + self.vmorph.morph_id
        response = self.client.get(url)
        actual = response.status_code
        expected = 404
        self.assertEqual(actual, expected)

    def test_retrieve(self):
        """
        """
        url = RESOURCE_URL + self.vmorph.morph_id.replace("/", URL_ENCODED_SOLIDUS)
        response = self.client.get(url)
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)

class FE6Unit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "FE6!Rutger"
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": True}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

    def test_retrieve(self):
        """
        """
        url = RESOURCE_URL + str(self.vmorph.id) + "/"
        response = self.client.get(url)
        actual = response.status_code
        expected = 200
        self.assertEqual(actual, expected)
        logger.debug("response.data: %r", response.data)

    def test_retrieve__fail(self):
        """
        """
        # first, confirm that vmorph.id does not exist.
        wmorph_id = 9999
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
        """
        # first, confirm that vmorph.id does not exist.
        wmorph_id = 9999
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

class FE7Unit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        morph_id = "FE7!Lyn"
        game_no = 7
        name = "Lyn"
        options = {"lyn_mode": True}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph


class FE8Unit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 8, "name": "Gerik"}
        game_no = 6
        name = "Marcus"
        options = {}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

class FE5Unit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 5, "name": "Mareeta"}
        game_no = 6
        name = "Marcus"
        options = {}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph


class FE9Unit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())
        kwargs = {"game_no": 5, "name": "Mareeta"}
        game_no = 6
        name = "Marcus"
        options = {}
        vmorph = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options)
        self.vmorph = vmorph

