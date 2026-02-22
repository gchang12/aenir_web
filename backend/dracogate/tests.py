"""
"""

import unittest
from unittest.mock import patch

from django.test import TestCase

from dracogate._logging import logger

RESOURCE_URL = "/dracogate/api/morphs/"

class NormalUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 6
        name = "Roy"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_that_invalid_options_are_ignored(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"invalid": "option"})
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)

    def test_get_morph__verify_success(self):
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

    def test_create_morph__blank_id(self):
        """
        Tests the morph-creation method.
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs["morph_id"] = ""
        with self.assertRaises(Exception):
            self.client.post(url, data=kwargs)

    def test_create_morph__duplicate_id(self):
        """
        Tests the morph-creation method.
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs["morph_id"] = "morph_id"
        self.client.post(url, data=kwargs)
        with self.assertRaises(Exception):
            self.client.post(url, data=kwargs)
        response = self.client.delete(url + f"{kwargs['morph_id']}/")

    def test_create_morph__max_length_exceeded(self):
        """
        Tests the morph-creation method.
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        for i in range(5):
            kwargs["morph_id"] = "my-morph%d" % i
            response = self.client.post(url, data=kwargs)
        with self.assertRaises(Exception):
            self.client.post(url, data=kwargs)
        # cleanup
        for i in range(5):
            kwargs["morph_id"] = "my-morph%d" % i
            response = self.client.delete(url + f"{kwargs['morph_id']}/")

    def test_create_and_delete_morph(self):
        """
        Tests the morph-creation method.
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs["morph_id"] = "my-morph"
        response = self.client.post(url, data=kwargs)
        data = response.data
        logger.debug("response.data: %r", data)
        response = self.client.delete(url + f"{kwargs['morph_id']}/")

    def test_delete_morph(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs["morph_id"] = "my-morph"
        response = self.client.delete(url + f"{kwargs['morph_id']}/")
        logger.debug("Morph has been deleted.")
        #logger.debug("response.data: %r", response.data)
        # If the deletion method didn't work, this should raise an error.
        response2 = self.client.post(url, data=kwargs)
        logger.debug("Morph with id=%r has been created.", response2.data['id'])

class FatheredUnit(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
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

    def test_get_morph__verify_success_alt(self):
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

    def test_get_morph__verify_error(self):
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

class HardModeUnit(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": "false"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
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

    def test_get_morph__verify_success_alt(self):
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

    def test_get_morph__verify_error(self):
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

class DeclinableUnit(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 6
        name = "Hugh"
        options = {"number_of_declines": 0}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
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

    def test_get_morph__verify_success_alt1(self):
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

    def test_get_morph__verify_success_alt2(self):
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

    def test_get_morph__verify_success_alt3(self):
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

    def test_get_morph__verify_error(self):
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

    def test_get_morph__verify_invalid_values(self):
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
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 6
        name = "Gonzales"
        options = {"hard_mode": "false", "route": "Lalum"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
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

    def test_get_morph__verify_success__elphin_no_hm(self):
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

    def test_get_morph__verify_success__lalum_hm(self):
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

    def test_get_morph__verify_success__elphin_hm(self):
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

    def test_get_morph__verify_error1(self):
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

    def test_get_morph__verify_error2(self):
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
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Lyn"
        options = {"lyn_mode": "false"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_error(self):
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

    def test_get_morph__verify_success__lyn_mode(self):
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

    def test_get_morph__verify_success__no_lyn_mode(self):
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
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Ninian"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)

    def test_get_morph__verify_server_failure(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "UNIT_DNE")

class Nils(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Nils"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
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

    def test_get_morph__verify_success_alt(self):
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
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 8
        name = "Lyon"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

class InvalidGame(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 10
        name = "Ike"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_error(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        expected = {"error"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)
        actual = response.data["error"]
        expected = "INVALID_GAME"
        self.assertEqual(actual, expected)

class InvalidUnit(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Marth"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_error(self):
        """
        """
        url = RESOURCE_URL
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        expected = {"error"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)
        actual = response.data["error"]
        expected = "UNIT_DNE"
        self.assertEqual(actual, expected)

# NOTE: POST

class NormalUnitPOST(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 6
        name = "Roy"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())
        self.client.post(URL, data=self.kwargs)

    def tearDown(self):
        """
        """
        morph_id = self.kwargs['morph_id']
        self.client.delete(URL + f"{morph_id}/")

class FatheredUnitPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())


class HardModeUnitPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": "false"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class DeclinableUnitPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 6
        name = "Hugh"
        options = {"number_of_declines": 0}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class GonzalesPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 6
        name = "Gonzales"
        options = {"hard_mode": "false", "route": "Lalum"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class LyndisLeaguePOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Lyn"
        options = {"lyn_mode": "false"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class NinianPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Ninian"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class NilsPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Nils"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class BonusUnitPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 8
        name = "Lyon"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class InvalidGamePOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 10
        name = "Ike"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

class InvalidUnitPOST(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

    def setUp(self):
        """
        """
        game_no = 7
        name = "Marth"
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

