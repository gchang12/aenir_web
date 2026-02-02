"""
"""

from django.test import TestCase

from aenir import get_morph

class NormalUnit(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 6
        name = "Roy"
        self.kwargs = {"game_no": game_no, "name": name}

    def test_create_morph(self):
        """
        """
        kwargs = self.kwargs
        response = self.client.get("/dracogate/api/morphs/", kwargs)

class HardModeUnit(TestCase):
    """
    """

class Gonzales(TestCase):
    """
    """

class FatheredUnit(TestCase):
    """
    """

class LyndisLeague(TestCase):
    """
    """
