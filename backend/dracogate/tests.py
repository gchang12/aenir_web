"""
"""

import unittest

from django.test import TestCase
from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError

from aenir import get_morph
from aenir._exceptions import (
    InitError,
)

from .models import (
    VirtualMorph,
    Stat,
)
from .forms import (
    InitFormBuilder,
)

from ._logging import logger

class VirtualMorphTests(TestCase):
    """
    """

    def test__progress_validation__okay(self):
        """
        """
        game_no = 6
        name = "Roy"
        progress = {
            "current_cls": "Lord",
            "current_lv": 1,
        }
        vmorph = VirtualMorph.objects.create(
            game_no=game_no,
            name=name,
            progress=progress,
            owner=None,
            morph_id="progress_validation",
        )

    @unittest.expectedFailure
    def test__progress_validation__type_err(self):
        """
        """
        game_no = 6
        name = "Roy"
        progress = [
            ("current_cls", "Lord"),
            ("current_lv", 1),
        ]
        with self.assertRaises(ValidationError):
            VirtualMorph.objects.create(
                game_no=game_no,
                name=name,
                progress=progress,
                owner=None,
                morph_id="progress_validation",
            )

    @unittest.expectedFailure
    def test__progress_validation__wrong_keys(self):
        """
        """
        game_no = 6
        name = "Roy"
        progress = {
            "current_cls": "Lord",
            "current_lv": 1,
            "": None,
        }
        with self.assertRaises(ValidationError):
            VirtualMorph.objects.create(
                game_no=game_no,
                name=name,
                progress=progress,
                owner=None,
                morph_id="progress_validation",
            )

    @unittest.expectedFailure
    def test__progress_validation__wrong_value_types(self):
        """
        """
        game_no = 6
        name = "Roy"
        progress = {
            "current_cls": "Lord",
            "current_lv": None,
        }
        with self.assertRaises(ValidationError):
            VirtualMorph.objects.create(
                game_no=game_no,
                name=name,
                progress=progress,
                owner=None,
                morph_id="progress_validation",
            )

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
            },
            {
                "id": "Pow",
                "current_val": 5.0,
                "growth_rate": 40,
                "max_val": 20.0,
                "absmax_val": 30.0,
            },
            {
                "id": "Skl",
                "current_val": 5.0,
                "growth_rate": 50,
                "max_val": 20.0,
                "absmax_val": 30.0,
            },
            {
                "id": "Spd",
                "current_val": 7.0,
                "growth_rate": 40,
                "max_val": 20.0,
                "absmax_val": 30.0,
            },
            {
                "id": "Lck",
                "current_val": 7.0,
                "growth_rate": 60,
                "max_val": 30.0,
                "absmax_val": 30.0,
            },
            {
                "id": "Def",
                "current_val": 5.0,
                "growth_rate": 25,
                "max_val": 20.0,
                "absmax_val": 30.0,
            },
            {
                "id": "Res",
                "current_val": 0.0,
                "growth_rate": 30,
                "max_val": 20.0,
                "absmax_val": 30.0,
            },
            {
                "id": "Con",
                "current_val": 6.0,
                "growth_rate": None,
                "max_val": 20.0,
                "absmax_val": 25.0,
            },
            {
                "id": "Mov",
                "current_val": 5.0,
                "growth_rate": None,
                "max_val": 15.0,
                "absmax_val": 15.0,
            },
        )
        actual = tuple(stat._asdict() for stat in vmorph._generate_stats())
        self.assertTupleEqual(actual, expected)

class InitFormBuilderTests(TestCase):
    """
    """

    @staticmethod
    def build_form_class(game_no, name):
        """
        """
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as err:
            init_params = err.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        return form_class

    def assertFieldsEqual(self, form_class, fields):
        """
        """
        actual = tuple(form_class.base_fields)
        expected = tuple(fields)
        self.assertTupleEqual(actual, expected)

    def assertFieldIsInstance(self, form_and_field, field_type):
        """
        """
        form_class, field_name = form_and_field
        field = form_class.base_fields[field_name]
        self.assertIsInstance(field, field_type)

    def assertChoicesEqual(self, form_and_field, choices):
        """
        """
        form_class, field_name = form_and_field
        field = form_class.base_fields[field_name]
        actual = tuple(field.choices)
        expected = tuple(choices)
        self.assertTupleEqual(actual, expected)

    def assertWidgetEqual(self, form_and_field, widget_type):
        """
        """
        form_class, field_name = form_and_field
        field = form_class.base_fields[field_name]
        self.assertIsInstance(field.widget, widget_type)

    def assertInitialEqual(self, form_and_field, expected):
        """
        """
        form_class, field_name = form_and_field
        field = form_class.base_fields[field_name]
        actual = field.initial
        self.assertEqual(actual, expected)

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def test_father(self):
        """
        """
        game_no = 4
        name = "Lakche"
        form_class = self.build_form_class(game_no, name)
        fields = ("game_no", "name", 'father')
        self.assertFieldsEqual(form_class, fields)
        widget_types = (
            forms.HiddenInput,
            forms.HiddenInput,
            forms.Select,
        )
        field_types = (
            forms.IntegerField,
            forms.CharField,
            forms.ChoiceField,
        )
        initial_values = (
            game_no,
            name,
            "Arden",
        )
        for field_name, field_type, widget_type, initial_value in zip(fields, field_types, widget_types, initial_values):
            with self.subTest(field_name=field_name):
                self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertWidgetEqual((form_class, field_name), widget_type)
                self.assertInitialEqual((form_class, field_name), initial_value)
        choices = (
            ('Arden', 'Arden'),
            ('Azel', 'Azel'),
            ('Alec', 'Alec'),
            ('Claude', 'Claude'),
            ('Jamka', 'Jamka'),
            ('Dew', 'Dew'),
            ('Noish', 'Noish'),
            ('Fin', 'Fin'),
            ('Beowolf', 'Beowolf'),
            ('Holyn', 'Holyn'),
            ('Midayle', 'Midayle'),
            ('Levin', 'Levin'),
            ('Lex', 'Lex'),
        )
        self.assertChoicesEqual((form_class, "father"), choices)

    def test_hard_mode(self):
        """
        """
        game_no = 6
        name = "Rutger"
        form_class = self.build_form_class(game_no, name)
        fields = ("game_no", "name", 'hard_mode')
        self.assertFieldsEqual(form_class, fields)
        widget_types = (
            forms.HiddenInput,
            forms.HiddenInput,
            forms.CheckboxInput,
        )
        field_types = (
            forms.IntegerField,
            forms.CharField,
            forms.BooleanField,
        )
        initial_values = (
            game_no,
            name,
            False,
        )
        for field_name, field_type, widget_type, initial_value in zip(fields, field_types, widget_types, initial_values):
            with self.subTest(field_name=field_name):
                self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertWidgetEqual((form_class, field_name), widget_type)
                self.assertInitialEqual((form_class, field_name), initial_value)

    def test_number_of_declines(self):
        """
        """
        game_no = 6
        name = "Hugh"
        form_class = self.build_form_class(game_no, name)
        fields = ("game_no", "name", 'number_of_declines')
        self.assertFieldsEqual(form_class, fields)
        widget_types = (
            forms.HiddenInput,
            forms.HiddenInput,
            forms.NumberInput,
        )
        field_types = (
            forms.IntegerField,
            forms.CharField,
            forms.IntegerField,
        )
        initial_values = (
            game_no,
            name,
            0,
        )
        for field_name, field_type, widget_type, initial_value in zip(fields, field_types, widget_types, initial_values):
            with self.subTest(field_name=field_name):
                self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertWidgetEqual((form_class, field_name), widget_type)
                self.assertInitialEqual((form_class, field_name), initial_value)

    def test_hard_mode__and__chapter(self):
        """
        """
        game_no = 6
        name = "Cath"
        form_class = self.build_form_class(game_no, name)
        fields = ("game_no", "name", 'hard_mode', 'chapter')
        self.assertFieldsEqual(form_class, fields)
        widget_types = (
            forms.HiddenInput,
            forms.HiddenInput,
            forms.CheckboxInput,
            forms.Select,
        )
        field_types = (
            forms.IntegerField,
            forms.CharField,
            forms.BooleanField,
            forms.ChoiceField,
        )
        initial_values = (
            game_no,
            name,
            False,
            "12",
        )
        for field_name, field_type, widget_type, initial_value in zip(fields, field_types, widget_types, initial_values):
            with self.subTest(field_name=field_name):
                self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertWidgetEqual((form_class, field_name), widget_type)
                self.assertInitialEqual((form_class, field_name), initial_value)
        choices = (
            ("12", "12"),
            ("16", "16"),
            ("20", "20"),
            ("22", "22"),
        )
        self.assertChoicesEqual((form_class, "chapter"), choices)

    def test_lyn_mode(self):
        """
        """
        game_no = 7
        name = "Wallace"
        form_class = self.build_form_class(game_no, name)
        fields = ("game_no", "name", 'lyn_mode')
        self.assertFieldsEqual(form_class, fields)
        widget_types = (
            forms.HiddenInput,
            forms.HiddenInput,
            forms.CheckboxInput,
        )
        field_types = (
            forms.IntegerField,
            forms.CharField,
            forms.BooleanField,
        )
        initial_values = (
            game_no,
            name,
            False,
        )
        for field_name, field_type, widget_type, initial_value in zip(fields, field_types, widget_types, initial_values):
            with self.subTest(field_name=field_name):
                self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertWidgetEqual((form_class, field_name), widget_type)
                self.assertInitialEqual((form_class, field_name), initial_value)

class UnitConfirmViewTests(TestCase):
    """
    """

    def check_response_and_vmorph_attributes(self, game_no, name, options):
        """
        """
        data = {
            "game_no": game_no,
            "name": name,
        }
        data.update(options)
        # send data
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.post(url, data=data)
        # check response code
        self.assertLess(response.status_code, 400)
        # check database for expected object.
        vmorph = VirtualMorph.objects.get()
        self.assertEqual(vmorph.game_no, game_no)
        self.assertEqual(vmorph.name, name)
        self.assertDictEqual(vmorph.options, options)
        self.assertTrue(vmorph.morph_id)

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def test_father(self):
        """
        Checks that VirtualMorph is created with expected attributes.
        """
        # prepare data
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        self.check_response_and_vmorph_attributes(game_no, name, options)

    def test_hard_mode(self):
        """
        Checks that VirtualMorph is created with expected attributes.
        """
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": True}
        self.check_response_and_vmorph_attributes(game_no, name, options)

    def test_number_of_declines(self):
        """
        Checks that VirtualMorph is created with expected attributes.
        """
        game_no = 6
        name = "Hugh"
        options = {"number_of_declines": 2}
        self.check_response_and_vmorph_attributes(game_no, name, options)

    def test_hard_mode__and__chapter(self):
        """
        Checks that VirtualMorph is created with expected attributes.
        """
        game_no = 6
        name = "Cath"
        options = {"hard_mode": True, "chapter": "20"}
        self.check_response_and_vmorph_attributes(game_no, name, options)

    def test_lyn_mode(self):
        """
        Checks that VirtualMorph is created with expected attributes.
        """
        game_no = 7
        name = "Wallace"
        options = {"lyn_mode": True}
        self.check_response_and_vmorph_attributes(game_no, name, options)

