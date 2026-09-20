"""
"""

from django.test import TestCase
import django.forms

from aenir import (
    get_morph,
    InitError,
)

from . import forms

class InitFormBuilderTests(TestCase):
    """
    """

    def test_father(self):
        """
        """
        try:
            get_morph(4, "Lakche")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = forms.InitFormBuilder.build_form_class(init_params)
        self.assertIn("father", form_class.declared_fields)
        field = form_class.declared_fields["father"]
        self.assertIsInstance(field, django.forms.ChoiceField)
        choices = init_params.pop("father")
        self.assertEqual(field.choices, [(choice, choice) for choice in choices])

    def test_hard_mode(self):
        """
        """
        try:
            get_morph(6, "Rutger")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = forms.InitFormBuilder.build_form_class(init_params)
        self.assertIn("hard_mode", form_class.declared_fields)
        field = form_class.declared_fields["hard_mode"]
        self.assertIsInstance(field, django.forms.NullBooleanField)

    def test_number_of_declines(self):
        """
        """
        try:
            get_morph(6, "Hugh")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = forms.InitFormBuilder.build_form_class(init_params)
        self.assertIn("number_of_declines", form_class.declared_fields)
        field = form_class.declared_fields["number_of_declines"]
        self.assertIsInstance(field, django.forms.IntegerField)
        self.assertEqual(field.min_value, 0)
        self.assertEqual(field.max_value, 3)

    def test_chapter(self):
        """
        """
        try:
            get_morph(6, "Gonzales")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = forms.InitFormBuilder.build_form_class(init_params)
        self.assertIn("hard_mode", form_class.declared_fields)
        self.assertIn("chapter", form_class.declared_fields)
        field = form_class.declared_fields["chapter"]
        self.assertIsInstance(field, django.forms.ChoiceField)
        choices = init_params.pop("chapter")
        self.assertEqual(field.choices, [(choice, choice) for choice in choices])

    def test_lyn_mode(self):
        """
        """
        try:
            get_morph(7, "Lyn")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = forms.InitFormBuilder.build_form_class(init_params)
        self.assertIn("lyn_mode", form_class.declared_fields)
        field = form_class.declared_fields["lyn_mode"]
        self.assertIsInstance(field, django.forms.NullBooleanField)

# TODO: Write forms to test init-preview.
