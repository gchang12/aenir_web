"""
"""

from django.test import TestCase

from dracogate.models import Morph
from dracogate._logging import logger

class NormalMorph(TestCase):
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

    def test_two_morphs_with_same_id_can_coexist_if_user_is_null(self):
        """
        """
        Morph.objects.create(morph_id="morph1", game_no=6, name="Roy"),
        Morph.objects.create(morph_id="morph1", game_no=6, name="Roy"),
        actual = Morph.objects.filter(morph_id="morph1").count()
        expected = 2
        self.assertEqual(actual, expected)
