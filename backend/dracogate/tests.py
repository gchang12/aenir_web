"""
"""

import unittest

from django.test import TestCase

from aenir import get_morph

from dracogate._logging import logger

class NormalUnit(TestCase):
    """
    """
    url = "/dracogate/api/morphs/"

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
        url = self.url
        kwargs = self.kwargs
        kwargs.update({"invalid": "option"})
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)

    def test_get_morph__verify_success(self):
        """
        """
        url = self.url
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
        url = self.url
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

    def test_get_morph__verify_error(self):
        """
        """
        url = self.url
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
        options = {"hard_mode": "true"}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
        """
        """
        url = self.url
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

    def test_get_morph__verify_error(self):
        """
        """
        url = self.url
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
        options = {"number_of_declines": 3}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
        """
        """
        url = self.url
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

    def test_get_morph__verify_invalid_values(self):
        """
        """
        url = self.url
        kwargs = self.kwargs
        kwargs["number_of_declines"] = 4
        response = self.client.get(url, data=kwargs)
        self.assertIn("missingParams", response.data)
        actual = set(response.data['missingParams'])
        expected = {"number_of_declines"}
        self.assertSetEqual(actual, expected)

    def test_get_morph__verify_error(self):
        """
        """
        url = self.url
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
        url = self.url
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

    def test_get_morph__verify_error1(self):
        """
        """
        url = self.url
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
        url = self.url
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
        url = self.url
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

    def test_get_morph__verify_success(self):
        """
        """
        url = self.url
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

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
        logger.debug("%s", self.id())

    def test_get_morph__verify_success(self):
        """
        """
        url = self.url
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

    def test_get_morph__verify_server_failure(self):
        """
        """
        url = self.url
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
        url = self.url
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "true"})
        response = self.client.get(url, data=kwargs)
        self.assertNotIn("missingParams", response.data)

    def test_get_morph__verify_server_failure(self):
        """
        """
        url = self.url
        kwargs = self.kwargs
        kwargs.update({"lyn_mode": "false"})
        response = self.client.get(url, data=kwargs)
        expected = {"unitClass", "level", "stats"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)

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
        url = self.url
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
        url = self.url
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
        url = self.url
        kwargs = self.kwargs
        response = self.client.get(url, data=kwargs)
        expected = {"error"}
        actual = set(response.data.keys())
        self.assertSetEqual(actual, expected)
        actual = response.data["error"]
        expected = "UNIT_DNE"
        self.assertEqual(actual, expected)

