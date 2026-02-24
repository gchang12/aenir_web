"""
"""

import unittest

from django.test import TestCase
from django.core.exceptions import ValidationError

from aenir_web._logging import logger

from dracogate.models import Morph

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
        morph = Morph.objects.create(morph_id=morph_id, **self.kwargs)
        actual = morph.options
        expected = {}
        logger.debug("morph.options: %r", morph.options)
        self.assertDictEqual(actual, expected)
        actual = morph.history
        expected = []
        logger.debug("morph.history: %r", morph.history)
        self.assertListEqual(actual, expected)
        actual = morph.user
        self.assertIsNone(actual)

    def test_two_morphs_with_same_id_can_coexist_if_user_is_null(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        morph1 = Morph.objects.create(morph_id=morph_id, **kwargs)
        morph2 = Morph.objects.create(morph_id=morph_id, **kwargs)
        actual = Morph.objects.filter(morph_id=morph_id).count()
        expected = 2
        self.assertEqual(actual, expected)
        morph1.full_clean()
        morph2.full_clean()

    def test_morph_can_have_blank_name(self):
        """
        """
        morph_id = ""
        kwargs = self.kwargs
        morph = Morph.objects.create(morph_id=morph_id, **kwargs)
        with self.assertRaises(ValidationError):
            morph.full_clean()
        logger.debug("At the model level, Morph can have blank 'morph_id' values; not so much at the form level.")

    def test_morph_cannot_have_blank_name(self):
        """
        """
        morph_id = self.morph_id
        kwargs = self.kwargs
        kwargs['name'] = ""
        morph = Morph.objects.create(morph_id=morph_id, **kwargs)
        with self.assertRaises(ValidationError):
            morph.full_clean()
