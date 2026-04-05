"""
"""

from django.test import TestCase

from aenir import get_morph

from .models import (
    VirtualMorph,
    Stat,
)

class VirtualMorphTests(TestCase):
    """
    """

    def test_generate_stats(self):
        """
        """
        game_no = 6
        name = "Roy"
        morph = get_morph(game_no, name)
        vmorph = VirtualMorph(game_no=game_no, name=name)
        vmorph.morph = morph
        expected = (
            {
                "id": "HP",
                "current_val": 18.0,
                "growth_rate": 80,
                "max_val": 60.0,
                "absmax_val": 80.0,
                "css_class": None,
            },
            {
                "id": "Pow",
                "current_val": 5.0,
                "growth_rate": 40,
                "max_val": 20.0,
                "absmax_val": 30.0,
                "css_class": None,
            },
            {
                "id": "Skl",
                "current_val": 5.0,
                "growth_rate": 50,
                "max_val": 20.0,
                "absmax_val": 30.0,
                "css_class": None,
            },
            {
                "id": "Spd",
                "current_val": 7.0,
                "growth_rate": 40,
                "max_val": 20.0,
                "absmax_val": 30.0,
                "css_class": None,
            },
            {
                "id": "Lck",
                "current_val": 7.0,
                "growth_rate": 60,
                "max_val": 30.0,
                "absmax_val": 30.0,
                "css_class": None,
            },
            {
                "id": "Def",
                "current_val": 5.0,
                "growth_rate": 25,
                "max_val": 20.0,
                "absmax_val": 30.0,
                "css_class": None,
            },
            {
                "id": "Res",
                "current_val": 0.0,
                "growth_rate": 30,
                "max_val": 20.0,
                "absmax_val": 30.0,
                "css_class": None,
            },
            {
                "id": "Con",
                "current_val": 6.0,
                "growth_rate": None,
                "max_val": 20.0,
                "absmax_val": 25.0,
                "css_class": None,
            },
            {
                "id": "Mov",
                "current_val": 5.0,
                "growth_rate": None,
                "max_val": 15.0,
                "absmax_val": 15.0,
                "css_class": None,
            },
        )
        actual = tuple(vmorph._generate_stats())
        self.assertTupleEqual(actual, expected)
