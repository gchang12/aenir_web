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
        options = {}
        kwargs = {"game_no": game_no, "name": name}
        kwargs.update(options)
        self.kwargs = kwargs

    def test_create_morph(self):
        """
        """
        kwargs = self.kwargs
        response = self.client.post("/dracogate/api/morphs/", data=kwargs)

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
