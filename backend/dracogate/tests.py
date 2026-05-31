"""
Tests functionality for storing, interacting with, and deleting Morph objects.
"""

import re
import unittest
import unittest.mock
import urllib.parse

from django.test import TestCase
from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError

from bs4 import BeautifulSoup

import aenir.games
import aenir.morph
from aenir import get_morph
from aenir._exceptions import (
    InitError,
    UnitNotFoundError,
)

from .models import (
    VirtualMorph,
)
from .forms import (
    InitFormBuilder,
)

from ._logging import logger

# MODELS #

class VirtualMorphTests(TestCase):
    """
    Tests functionality of database-representation of Morph.
    """

    def test__progress_validation__okay(self):
        """
        Demo: Creating VirtualMorph with minimal parameters.
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

    def test_generate_morph_id(self):
        """
        Asserts that 'morph_id' generated is of expected pattern.
        """
        game_no = 4
        name = "Sigurd"
        pattern = "FE[4-9]!Sigurd-[0-9]{4}_[0-9]{6}"
        morph_id = VirtualMorph._generate_morph_id(game_no, name)
        actual = re.fullmatch(pattern, morph_id)
        self.assertIsNotNone(actual)

    def test_generate_stats(self):
        """
        Asserts that value of stats yielded are as expected.
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

    def test_save(self):
        """
        Asserts that progress-saving functionality of augmented 'save' method works.
        """
        game_no = 4
        name = "Levin"
        morph = get_morph(game_no, name)
        morph.current_cls = "Reaper"
        morph.current_lv = -1
        vmorph = VirtualMorph(
            morph_id="test_save",
            game_no=game_no,
            name=name,
        )
        vmorph.morph = morph
        vmorph.save()
        vmorph2 = VirtualMorph.objects.get()
        self.assertEqual(vmorph2.progress['current_cls'], morph.current_cls)
        self.assertEqual(vmorph2.progress['current_lv'], morph.current_lv)

# FORMS #

class InitFormBuilderTests(TestCase):
    """
    Tests functionality of dynamic forms.
    """

    def setUp(self):
        """
        Logs current test-ID.
        """
        logger.debug("%s", self.id())

    def test_father(self):
        """
        Checks the attributes of a form that has a field for the 'father' option.
        """
        game_no = 4
        name = "Lakche"
        #form_class = self.build_form_class(game_no, name)
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as err:
            init_params = err.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        fields = ("game_no", "name", 'father')
        #self.assertFieldsEqual(form_class, fields)
        actual = tuple(form_class.base_fields)
        expected = tuple(fields)
        self.assertTupleEqual(actual, expected)
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
            field = form_class.base_fields[field_name]
            actual = field.initial
            expected = initial_value
            with self.subTest(field_name=field_name):
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertIsInstance(field, field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #field = form_class.base_fields[field_name]
                self.assertIsInstance(field.widget, widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #field = form_class.base_fields[field_name]
                self.assertEqual(actual, expected)
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
        #self.assertChoicesEqual((form_class, "father"), choices)
        field_name = "father"
        field = form_class.base_fields[field_name]
        actual = field.choices
        expected = choices
        self.assertSequenceEqual(actual, expected)

    def test_hard_mode(self):
        """
        Checks the attributes of a form that has a field for the 'hard_mode' option.
        """
        game_no = 6
        name = "Rutger"
        #form_class = self.build_form_class(game_no, name)
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as err:
            init_params = err.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        fields = ("game_no", "name", 'hard_mode')
        #self.assertFieldsEqual(form_class, fields)
        actual = tuple(form_class.base_fields)
        expected = tuple(fields)
        self.assertTupleEqual(actual, expected)
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
            field = form_class.base_fields[field_name]
            actual = field.initial
            expected = initial_value
            with self.subTest(field_name=field_name):
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertIsInstance(field, field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #field = form_class.base_fields[field_name]
                self.assertIsInstance(field.widget, widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #field = form_class.base_fields[field_name]
                self.assertEqual(actual, expected)

    def test_number_of_declines(self):
        """
        Checks the attributes of a form that has a field for the 'number_of_declines' option.
        """
        game_no = 6
        name = "Hugh"
        #form_class = self.build_form_class(game_no, name)
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as err:
            init_params = err.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        fields = ("game_no", "name", 'number_of_declines')
        #self.assertFieldsEqual(form_class, fields)
        actual = tuple(form_class.base_fields)
        expected = tuple(fields)
        #logger.debug("actual %r", actual)
        self.assertTupleEqual(actual, expected)
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
            field = form_class.base_fields[field_name]
            actual = field.initial
            expected = initial_value
            with self.subTest(field_name=field_name):
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertIsInstance(field, field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #field = form_class.base_fields[field_name]
                self.assertIsInstance(field.widget, widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #field = form_class.base_fields[field_name]
                self.assertEqual(actual, expected)

    def test_hard_mode__and__chapter(self):
        """
        Checks the attributes of a form that has a field for the 'hard_mode' and 'chapter' options.
        """
        game_no = 6
        name = "Cath"
        #form_class = self.build_form_class(game_no, name)
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as err:
            init_params = err.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        fields = ("game_no", "name", 'hard_mode', 'chapter')
        #self.assertFieldsEqual(form_class, fields)
        actual = tuple(form_class.base_fields)
        expected = tuple(fields)
        self.assertTupleEqual(actual, expected)
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
            field = form_class.base_fields[field_name]
            actual = field.initial
            expected = initial_value
            with self.subTest(field_name=field_name):
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertIsInstance(field, field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #field = form_class.base_fields[field_name]
                self.assertIsInstance(field.widget, widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #field = form_class.base_fields[field_name]
                self.assertEqual(actual, expected)
        choices = (
            ("12", "12"),
            ("16", "16"),
            ("20", "20"),
            ("22", "22"),
        )
        #self.assertChoicesEqual((form_class, "chapter"), choices)
        field_name = "chapter"
        field = form_class.base_fields[field_name]
        actual = field.choices
        expected = choices
        self.assertSequenceEqual(actual, expected)

    def test_lyn_mode(self):
        """
        Checks the attributes of a form that has a field for the 'lyn_mode' options.
        """
        game_no = 7
        name = "Wallace"
        #form_class = self.build_form_class(game_no, name)
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as err:
            init_params = err.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        fields = ("game_no", "name", 'lyn_mode')
        #self.assertFieldsEqual(form_class, fields)
        actual = tuple(form_class.base_fields)
        expected = tuple(fields)
        self.assertTupleEqual(actual, expected)
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
            field = form_class.base_fields[field_name]
            actual = field.initial
            expected = initial_value
            with self.subTest(field_name=field_name):
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #self.assertFieldIsInstance((form_class, field_name), field_type)
                self.assertIsInstance(field, field_type)
                #self.assertWidgetEqual((form_class, field_name), widget_type)
                #field = form_class.base_fields[field_name]
                self.assertIsInstance(field.widget, widget_type)
                #self.assertInitialEqual((form_class, field_name), initial_value)
                #field = form_class.base_fields[field_name]
                self.assertEqual(actual, expected)

# VIEWS #

class GameSelectViewTests(TestCase):
    """
    Checks if hyperlinks are displayed.
    """

    def test_hyperlinks_exist_and_work(self):
        """
        Checks if a hyperlink for each unit_select-view is displayed.
        """
        url = reverse("dracogate:game_select")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.text, 'html.parser')
        for fe_game in aenir.games.FireEmblemGame:
            game_no = fe_game.value
            unit_select_url = reverse("dracogate:unit_select", args=[game_no]) + "#FE%d" % game_no
            css_selector = "a[href='%s']" % unit_select_url
            a = soup.css.select_one(css_selector)
            logger.debug("Checking if '%s' exists in HTML document.", css_selector)
            with self.subTest(fe_game=game_no):
                self.assertIsNotNone(a)

class UnitSelectViewTests(TestCase):
    """
    Checks if hyperlinks are displayed.
    """

    def test_hyperlinks_exist_and_work(self):
        """
        Checks if a hyperlink for each unit_confirm-view is displayed.
        """
        for fe_game in aenir.games.FireEmblemGame:
            game_no = fe_game.value
            morph_cls = getattr(aenir.morph, "Morph%d" % game_no)
            url = reverse("dracogate:unit_select", args=[game_no])
            response = self.client.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            with self.subTest(fe_game=game_no):
                self.assertEqual(response.status_code, 200)
                for name in morph_cls.get_true_character_list():
                    unit_confirm_url = reverse("dracogate:unit_confirm", args=[game_no, name]) + "#FE%d" % game_no
                    css_selector = 'a[href="%s"]' % unit_confirm_url
                    logger.debug("Checking if '%s' exists in HTML document.", css_selector)
                    a = soup.css.select_one(css_selector)
                    self.assertIsNotNone(a)

    def test_game_dne(self):
        """
        Validates that nonexistent games are not covered by application.
        """
        game_no = 99
        url = reverse("dracogate:unit_select", args=[game_no])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class UnitConfirmViewTests(TestCase):
    """
    Checks that units are created upon successful POST request.
    """

    def setUp(self):
        """
        Logs current test-ID.
        """
        logger.debug("%s", self.id())

    def test_father(self):
        """
        Checks that VirtualMorph that requires 'father' value is created with expected attributes.
        """
        # prepare data
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
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

    def test_hard_mode(self):
        """
        Checks that VirtualMorph that requires 'hard_mode' value is created with expected attributes.
        """
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": True}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
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

    def test_number_of_declines(self):
        """
        Checks that VirtualMorph that requires 'number_of_declines' value is created with expected attributes.
        """
        game_no = 6
        name = "Hugh"
        options = {"number_of_declines": 2}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
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

    def test_hard_mode__and__chapter(self):
        """
        Checks that VirtualMorph that requires 'hard_mode' and 'chapter' values is created with expected attributes.
        """
        game_no = 6
        name = "Cath"
        options = {"hard_mode": True, "chapter": "20"}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
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

    def test_lyn_mode(self):
        """
        Checks that VirtualMorph that requires 'lyn_mode' value is created with expected attributes.
        """
        game_no = 7
        name = "Wallace"
        options = {"lyn_mode": True}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
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

    def test_father__GET(self):
        """
        Checks that GET response contains <select> element for 'father'.
        """
        # prepare data
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
        data = {
            "game_no": game_no,
            "name": name,
        }
        data.update(options)
        # send data
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.get(url, data=data)
        # check response code
        self.assertEqual(response.status_code, 200)
        # check form for correct widgets and the like.
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.css.select_one('form[action="%s"]' % url)
        self.assertIsNotNone(form)
        select = form.css.select_one("select[name='father']")
        self.assertIsNotNone(select)
        morph_cls = aenir.morph.Morph4
        for father in morph_cls.FATHER_LIST():
            option = select.css.select_one("option[value='%s']" % father)
            self.assertIsNotNone(option)
        for option in select.find_all("option"):
            self.assertIn(option['value'], morph_cls.FATHER_LIST())

    def test_hard_mode__GET(self):
        """
        Checks that GET response contains <input> element for 'hard_mode'.
        """
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": True}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
        data = {
            "game_no": game_no,
            "name": name,
        }
        data.update(options)
        # send data
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.get(url, data=data)
        # check response code
        self.assertEqual(response.status_code, 200)
        # check form for correct widgets and the like.
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.css.select_one('form[action="%s"]' % url)
        self.assertIsNotNone(form)
        input1 = form.css.select_one("input[type='checkbox'][name='hard_mode']")
        self.assertIsNotNone(input1)

    def test_number_of_declines__GET(self):
        """
        Checks that GET response contains <input> element for 'number_of_declines'.
        """
        game_no = 6
        name = "Hugh"
        options = {"number_of_declines": 2}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
        data = {
            "game_no": game_no,
            "name": name,
        }
        data.update(options)
        # send data
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.get(url, data=data)
        # check response code
        self.assertEqual(response.status_code, 200)
        # check form for correct widgets and the like.
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.css.select_one('form[action="%s"]' % url)
        self.assertIsNotNone(form)
        input1 = form.css.select_one("input[type='number'][name='number_of_declines']")
        self.assertIsNotNone(input1)
        self.assertEqual(input1['min'], "0")
        self.assertEqual(input1['max'], "3")

    def test_hard_mode__and__chapter__GET(self):
        """
        Checks that GET response contains <input> element for 'hard_mode' and <select> element for 'chapter'.
        """
        game_no = 6
        name = "Cath"
        options = {"hard_mode": True, "chapter": "20"}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
        data = {
            "game_no": game_no,
            "name": name,
        }
        data.update(options)
        # send data
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.get(url, data=data)
        # check response code
        self.assertEqual(response.status_code, 200)
        # check form for correct widgets and the like.
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.css.select_one('form[action="%s"]' % url)
        self.assertIsNotNone(form)
        input1 = form.css.select_one("input[type='checkbox'][name='hard_mode']")
        self.assertIsNotNone(input1)
        select = form.css.select_one("select[name='chapter']")
        self.assertIsNotNone(select)
        chapters = (
            "12",
            "16",
            "20",
            "22",
        )
        for chapter in chapters:
            option = form.css.select_one("option[value='%s']" % chapter)
            self.assertIsNotNone(option)
        for option in select.find_all("option"):
            self.assertIn(option['value'], chapters)

    def test_lyn_mode__GET(self):
        """
        Checks that GET response contains <input> element for 'lyn_mode'.
        """
        game_no = 7
        name = "Wallace"
        options = {"lyn_mode": True}
        #self.check_response_and_vmorph_attributes(game_no, name, options)
        data = {
            "game_no": game_no,
            "name": name,
        }
        data.update(options)
        # send data
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.get(url, data=data)
        # check response code
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.css.select_one('form[action="%s"]' % url)
        self.assertIsNotNone(form)
        input1 = form.css.select_one("input[type='checkbox'][name='lyn_mode']")
        self.assertIsNotNone(input1)

    def test_unit_dne(self):
        """
        Validates that nonexistent units for a given name are not covered.
        """
        game_no = 7
        name = "Marth"
        url = reverse("dracogate:unit_confirm", args=[game_no, name])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

class UnitConfirmPreviewViewTests(TestCase):
    """
    Checks that right unit data is displayed.
    """

    def setUp(self):
        """
        Logs current test-ID.
        """
        logger.debug("%s", self.id())

    def test_fe4_unit(self):
        """
        Checks that necessary information is displayed.
        """
        # declare parameters
        game_no = 4
        name = "Lakche"
        options = {"father": "Lex"}
        cls_lv = [
            ("Class", "Swordfighter"),
            ("Lv", "1"),
        ]
        url = reverse("dracogate:unit_confirm_preview", args=[game_no, name])
        # send request
        logger.debug("Sending request to '%s' with params: %r", url, options)
        response = self.client.get(url, query_params=options)
        self.assertEqual(response.status_code, 200)
        # check response body for expected elements.
        logger.debug("Checking response body for expected elements.")
        soup = BeautifulSoup(response.text, "html.parser")
        # class and level
        table1 = soup.css.select_one("table.class.level")
        self.assertIsNotNone(table1)
        for index_no, tr in enumerate(table1.css.select("thead > tr")):
            (key, value) = cls_lv[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, value)
        # create morph
        morph = get_morph(game_no, name, **options)
        # HP and all the other stats
        table2 = soup.css.select_one("table.numeric_stats")
        self.assertIsNotNone(table2)
        current_stats = morph.current_stats.as_list()
        for index_no, tr in enumerate(table2.css.select("tbody > tr")):
            (key, value) = current_stats[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, "%s" % (value / 100))
        # figure
        figure = soup.find("figure")
        self.assertIsNotNone(figure)
        # name
        h3 = figure.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, name)
        # image, maybe
        img = figure.find("img")
        self.assertIsNotNone(img)
        self.assertEqual(img['src'], "/static/dracogate/images/%d/characters/%s.png" % (game_no, name))

    def test_fe5_unit(self):
        """
        Checks that necessary information is displayed.
        """
        # declare parameters
        game_no = 5
        name = "Leaf"
        options = {}
        cls_lv = [
            ("Class", "Lord"),
            ("Lv", "1"),
        ]
        url = reverse("dracogate:unit_confirm_preview", args=[game_no, name])
        # send request
        logger.debug("Sending request to '%s' with params: %r", url, options)
        response = self.client.get(url, query_params=options)
        self.assertEqual(response.status_code, 200)
        # check response body for expected elements.
        logger.debug("Checking response body for expected elements.")
        soup = BeautifulSoup(response.text, "html.parser")
        # class and level
        table1 = soup.css.select_one("table.class.level")
        self.assertIsNotNone(table1)
        for index_no, tr in enumerate(table1.css.select("thead > tr")):
            (key, value) = cls_lv[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, value)
        # create morph
        morph = get_morph(game_no, name, **options)
        # HP and all the other stats
        table2 = soup.css.select_one("table.numeric_stats")
        self.assertIsNotNone(table2)
        current_stats = morph.current_stats.as_list()
        for index_no, tr in enumerate(table2.css.select("tbody > tr")):
            (key, value) = current_stats[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, "%s" % (value / 100))
        # figure
        figure = soup.find("figure")
        self.assertIsNotNone(figure)
        # name
        h3 = figure.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, name)
        # image, maybe
        img = figure.find("img")
        self.assertIsNotNone(img)
        self.assertEqual(img['src'], "/static/dracogate/images/%d/characters/%s.png" % (game_no, name))

    def test_fe6_unit(self):
        """
        Checks that necessary information is displayed.
        """
        # declare parameters
        game_no = 6
        name = "Rutger"
        options = {"hard_mode": "on"}
        cls_lv = [
            ("Class", "Myrmidon"),
            ("Lv", "4"),
        ]
        url = reverse("dracogate:unit_confirm_preview", args=[game_no, name])
        # send request
        logger.debug("Sending request to '%s' with params: %r", url, options)
        response = self.client.get(url, query_params=options)
        self.assertEqual(response.status_code, 200)
        # check response body for expected elements.
        logger.debug("Checking response body for expected elements.")
        soup = BeautifulSoup(response.text, "html.parser")
        # class and level
        table1 = soup.css.select_one("table.class.level")
        self.assertIsNotNone(table1)
        for index_no, tr in enumerate(table1.css.select("thead > tr")):
            (key, value) = cls_lv[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, value)
        # create morph
        options['hard_mode'] = True
        morph = get_morph(game_no, name, **options)
        # HP and all the other stats
        table2 = soup.css.select_one("table.numeric_stats")
        self.assertIsNotNone(table2)
        current_stats = morph.current_stats.as_list()
        for index_no, tr in enumerate(table2.css.select("tbody > tr")):
            (key, value) = current_stats[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, "%s" % (value / 100))
        # figure
        figure = soup.find("figure")
        self.assertIsNotNone(figure)
        # name
        h3 = figure.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, name)
        # image, maybe
        img = figure.find("img")
        self.assertIsNotNone(img)
        self.assertEqual(img['src'], "/static/dracogate/images/%d/characters/%s.png" % (game_no, name))

    def test_fe7_unit(self):
        """
        Checks that necessary information is displayed.
        """
        # declare parameters
        game_no = 7
        name = "Guy"
        options = {"hard_mode": "on"}
        cls_lv = [
            ("Class", "Myrmidon"),
            ("Lv", "3"),
        ]
        url = reverse("dracogate:unit_confirm_preview", args=[game_no, name])
        # send request
        logger.debug("Sending request to '%s' with params: %r", url, options)
        response = self.client.get(url, query_params=options)
        self.assertEqual(response.status_code, 200)
        # check response body for expected elements.
        logger.debug("Checking response body for expected elements.")
        soup = BeautifulSoup(response.text, "html.parser")
        # class and level
        table1 = soup.css.select_one("table.class.level")
        self.assertIsNotNone(table1)
        for index_no, tr in enumerate(table1.css.select("thead > tr")):
            (key, value) = cls_lv[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, value)
        # create morph
        options['hard_mode'] = True
        morph = get_morph(game_no, name, **options)
        # HP and all the other stats
        table2 = soup.css.select_one("table.numeric_stats")
        self.assertIsNotNone(table2)
        current_stats = morph.current_stats.as_list()
        for index_no, tr in enumerate(table2.css.select("tbody > tr")):
            (key, value) = current_stats[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, "%s" % (value / 100))
        # figure
        figure = soup.find("figure")
        self.assertIsNotNone(figure)
        # name
        h3 = figure.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, name)
        # image, maybe
        img = figure.find("img")
        self.assertIsNotNone(img)
        self.assertEqual(img['src'], "/static/dracogate/images/%d/characters/%s.png" % (game_no, name))

    def test_fe8_unit(self):
        """
        Checks that necessary information is displayed.
        """
        # declare parameters
        game_no = 8
        name = "Eirika"
        options = {}
        cls_lv = [
            ("Class", "Lord"),
            ("Lv", "1"),
        ]
        url = reverse("dracogate:unit_confirm_preview", args=[game_no, name])
        # send request
        logger.debug("Sending request to '%s' with params: %r", url, options)
        response = self.client.get(url, query_params=options)
        self.assertEqual(response.status_code, 200)
        # check response body for expected elements.
        logger.debug("Checking response body for expected elements.")
        soup = BeautifulSoup(response.text, "html.parser")
        # class and level
        table1 = soup.css.select_one("table.class.level")
        self.assertIsNotNone(table1)
        for index_no, tr in enumerate(table1.css.select("thead > tr")):
            (key, value) = cls_lv[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, value)
        # create morph
        morph = get_morph(game_no, name, **options)
        # HP and all the other stats
        table2 = soup.css.select_one("table.numeric_stats")
        self.assertIsNotNone(table2)
        current_stats = morph.current_stats.as_list()
        for index_no, tr in enumerate(table2.css.select("tbody > tr")):
            (key, value) = current_stats[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, "%s" % (value / 100))
        # figure
        figure = soup.find("figure")
        self.assertIsNotNone(figure)
        # name
        h3 = figure.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, name)
        # image, maybe
        img = figure.find("img")
        self.assertIsNotNone(img)
        self.assertEqual(img['src'], "/static/dracogate/images/%d/characters/%s.png" % (game_no, name))

    def test_fe9_unit(self):
        """
        Checks that necessary information is displayed.
        """
        # declare parameters
        game_no = 9
        name = "Titania"
        options = {}
        cls_lv = [
            ("Class", "Paladin"),
            ("Lv", "1"),
        ]
        url = reverse("dracogate:unit_confirm_preview", args=[game_no, name])
        # send request
        logger.debug("Sending request to '%s' with params: %r", url, options)
        response = self.client.get(url, query_params=options)
        self.assertEqual(response.status_code, 200)
        # check response body for expected elements.
        logger.debug("Checking response body for expected elements.")
        soup = BeautifulSoup(response.text, "html.parser")
        # class and level
        table1 = soup.css.select_one("table.class.level")
        self.assertIsNotNone(table1)
        for index_no, tr in enumerate(table1.css.select("thead > tr")):
            (key, value) = cls_lv[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, value)
        # create morph
        morph = get_morph(game_no, name, **options)
        # HP and all the other stats
        table2 = soup.css.select_one("table.numeric_stats")
        self.assertIsNotNone(table2)
        current_stats = morph.current_stats.as_list()
        for index_no, tr in enumerate(table2.css.select("tbody > tr")):
            (key, value) = current_stats[index_no]
            th = tr.find("th")
            self.assertIsNotNone(th)
            self.assertEqual(th.text, key)
            td = tr.find("td")
            self.assertIsNotNone(td)
            self.assertEqual(td.text, "%s" % (value / 100))
        # figure
        figure = soup.find("figure")
        self.assertIsNotNone(figure)
        # name
        h3 = figure.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, name)
        # image, maybe
        img = figure.find("img")
        self.assertIsNotNone(img)
        self.assertEqual(img['src'], "/static/dracogate/images/%d/characters/%s.png" % (game_no, name))

class ListMorphsViewTests(TestCase):
    """
    Checks to see if the expected elements are there.
    """

    def setUp(self):
        """
        Logs current test-ID and creates VirtualMorph objects.
        """
        logger.debug("%s", self.id())
        num_morphs = 50
        self.create_virtual_morph(num_morphs)
        self.url = reverse("dracogate:list_morphs")

    @staticmethod
    def create_virtual_morph(num_morphs):
        """
        Creates VirtualMorph objects given the number to create.
        """
        owner = None
        game_no = 6
        name = "Roy"
        options = {}
        progress = {
            "current_cls": "Lord",
            "current_lv": 1,
        }
        for i in range(num_morphs):
            morph_id = "FE6.Roy-%d" % (i + 1)
            VirtualMorph.objects.create(
                owner=owner,
                morph_id=morph_id,
                game_no=game_no,
                name=name,
                options=options,
                progress=progress,
            )

    def test_at_most_50_morphs(self):
        """
        Checks that page navigational elements are missing whenever max pagination count is not exceeded.
        """
        response = self.client.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.css.select_one(".page-navi a")
        self.assertIsNone(a)

    def test_more_than_50_morphs(self):
        """
        Checks that 'Next' navigational element is here if max pagination count is exceeded.
        """
        # next is present.
        self.create_virtual_morph(1)
        response = self.client.get(self.url + "?page=1")
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.css.select_one(".page-navi a[href='?page=2']")
        self.assertIsNotNone(a)

    def test_more_than_50_morphs__page2(self):
        """
        Checks that 'Previous' navigational element is here if max pagination count is exceeded.
        """
        # previous is present.
        self.create_virtual_morph(1)
        response = self.client.get(self.url + "?page=2")
        soup = BeautifulSoup(response.text, 'html.parser')
        a = soup.css.select_one("#list_morphs a")
        self.assertIsNotNone(a)
        h3 = a.find("h3")
        self.assertIsNotNone(h3)
        self.assertEqual(h3.text, "Morph ID: FE6.Roy-1")
        a2 = soup.css.select_one(".page-navi a[href='?page=1']")
        self.assertIsNotNone(a2)

# TODO: Implement!

class ModifyMorphViewTests(TestCase):
    """
    """
