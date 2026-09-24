"""
"""

#import json
#import html

import unittest

from django.test import TestCase
import django.forms
from django.urls import reverse
from django.contrib.auth import get_user_model

from aenir import (
    get_morph,
    InitError,
    GrowthsItemError,
)

from dracogate.forms import (
    InitFormBuilder,
    #LevelUpFormBuilder,
    ActionFormBuilder,
)
from dracogate.models import VirtualMorph

User = get_user_model()

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
        form_class = InitFormBuilder.build_form_class(init_params)
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
        form_class = InitFormBuilder.build_form_class(init_params)
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
        form_class = InitFormBuilder.build_form_class(init_params)
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
        form_class = InitFormBuilder.build_form_class(init_params)
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
        form_class = InitFormBuilder.build_form_class(init_params)
        self.assertIn("lyn_mode", form_class.declared_fields)
        field = form_class.declared_fields["lyn_mode"]
        self.assertIsInstance(field, django.forms.NullBooleanField)

# TODO: Write forms to test init-preview.

class UnitConfirmForecastTests(TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.generate_url = lambda game_no, name: reverse("dracogate:unit_confirm_forecast", kwargs={"game_no": game_no, "unit": name})

    def test_father(self):
        """
        """
        game_no = 4
        name = "Lakche"
        query_params = {"father": "Holyn"}
        old_values = ("31.0", "65")
        new_values = ("31.0", "135")
        url = self.generate_url(game_no, name)
        response = self.client.get(url, query_params=query_params)
        for value in new_values:
            self.assertContains(response, value)
        response = self.client.get(url)
        for value in old_values:
            self.assertContains(response, value)

    def test_hard_mode(self):
        """
        """
        game_no = 6
        name = "Rutger"
        query_params = {"hard_mode": "True"}
        old_values = ("22.0", "13.0")
        new_values = ("25.5", "8.75")
        url = self.generate_url(game_no, name)
        response = self.client.get(url, query_params=query_params)
        for value in new_values:
            self.assertContains(response, value)
        response = self.client.get(url)
        for value in old_values:
            self.assertContains(response, value)

    def test_number_of_declines(self):
        """
        """
        game_no = 6
        name = "Hugh"
        query_params = {"number_of_declines": "3"}
        old_values = ("26.0", "13.0")
        new_values = ("23.0", "10.0")
        url = self.generate_url(game_no, name)
        response = self.client.get(url, query_params=query_params)
        for value in new_values:
            self.assertContains(response, value)
        response = self.client.get(url)
        for value in old_values:
            self.assertContains(response, value)

    def test_chapter(self):
        """
        """
        game_no = 6
        name = "Cath"
        query_params = {"hard_mode": "True", "chapter": "22"}
        old_values = ("16.0", "11.0")
        new_values = ("22.3", "16.6")
        url = self.generate_url(game_no, name)
        response = self.client.get(url, query_params=query_params)
        for value in new_values:
            self.assertContains(response, value)
        response = self.client.get(url)
        for value in old_values:
            self.assertContains(response, value)

    def test_lyn_mode(self):
        """
        """
        game_no = 7
        name = "Wallace"
        query_params = {"lyn_mode": "True"}
        old_values = ("General (M)", "34.0")
        new_values = ("Knight", "30.0")
        url = self.generate_url(game_no, name)
        response = self.client.get(url, query_params=query_params)
        for value in new_values:
            self.assertContains(response, value)
        response = self.client.get(url)
        for value in old_values:
            self.assertContains(response, value)

class InitFormBuilderTests(TestCase):
    """
    """

    def test_father(self):
        """
        """
        data = {"father": "Lex"}
        try:
            get_morph(4, "Lakche")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(init_params)
        form = form_class(data)
        self.assertIs(form.is_valid(), True)
        self.assertDictEqual(form.cleaned_data, data)

    def test_hard_mode(self):
        """
        """
        data = {"hard_mode": True}
        try:
            get_morph(6, "Rutger")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(init_params)
        form = form_class(data)
        self.assertIs(form.is_valid(), True)
        self.assertDictEqual(form.cleaned_data, data)

    def test_number_of_declines(self):
        """
        """
        data = {"number_of_declines": 3}
        try:
            get_morph(6, "Hugh")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(init_params)
        form = form_class(data)
        self.assertIs(form.is_valid(), True)
        self.assertDictEqual(form.cleaned_data, data)

    def test_chapter(self):
        """
        """
        data = {"hard_mode": True, "chapter": "22"}
        try:
            get_morph(6, "Cath")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(init_params)
        form = form_class(data)
        self.assertIs(form.is_valid(), True)
        self.assertDictEqual(form.cleaned_data, data)

    def test_lyn_mode(self):
        """
        """
        data = {"lyn_mode": True}
        try:
            get_morph(7, "Lyn")
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(init_params)
        form = form_class(data)
        self.assertIs(form.is_valid(), True)
        self.assertDictEqual(form.cleaned_data, data)

class UnitConfirmTests(TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.generate_url = lambda game_no, name: reverse("dracogate:unit_confirm", kwargs={"game_no": game_no, "unit": name})
        self.user = User.objects.create()
        self.client.force_login(self.user)
        #print(type(self.user))
        #self.assertFalse(VirtualMorph.objects.all())

    def test_father(self):
        """
        """
        data = {"father": "Lex"}
        kwargs = {
            "game_no": 4,
            "name": "Lakche",
        }
        url = self.generate_url(**kwargs)
        response = self.client.post(url, data=data)
        self.assertEqual(VirtualMorph.objects.count(), 1)
        vmorph = VirtualMorph.objects.get()
        self.assertEqual(vmorph.owner, self.user)
        self.assertTrue(vmorph.name)
        self.assertEqual(vmorph.game_no, kwargs['game_no'])
        self.assertEqual(vmorph.unit, kwargs['name'])
        self.assertEqual(vmorph.init_options, data)
        # test for existence of init_options in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        response = self.client.get(url)
        values = (
            "Game",
            "FE%d" % kwargs['game_no'],
            "Unit",
            kwargs["name"],
            "Father",
            "Lex",
        )
        for value in values:
            self.assertContains(response, value)

    def test_hard_mode(self):
        """
        """
        data = {"hard_mode": True}
        kwargs = {
            "game_no": 6,
            "name": "Rutger",
        }
        url = self.generate_url(**kwargs)
        response = self.client.post(url, data=data)
        self.assertEqual(VirtualMorph.objects.count(), 1)
        vmorph = VirtualMorph.objects.get()
        self.assertEqual(vmorph.owner, self.user)
        self.assertTrue(vmorph.name)
        self.assertEqual(vmorph.game_no, kwargs['game_no'])
        self.assertEqual(vmorph.unit, kwargs['name'])
        self.assertEqual(vmorph.init_options, data)
        # test for existence of init_options in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        response = self.client.get(url)
        values = (
            "Game",
            "FE%d" % kwargs['game_no'],
            "Unit",
            kwargs["name"],
            "Difficulty",
            "Hard",
        )
        for value in values:
            self.assertContains(response, value)

    def test_number_of_declines(self):
        """
        """
        data = {"number_of_declines": 3}
        kwargs = {
            "game_no": 6,
            "name": "Hugh",
        }
        url = self.generate_url(**kwargs)
        response = self.client.post(url, data=data)
        self.assertEqual(VirtualMorph.objects.count(), 1)
        vmorph = VirtualMorph.objects.get()
        self.assertEqual(vmorph.owner, self.user)
        self.assertTrue(vmorph.name)
        self.assertEqual(vmorph.game_no, kwargs['game_no'])
        self.assertEqual(vmorph.unit, kwargs['name'])
        self.assertEqual(vmorph.init_options, data)
        # test for existence of init_options in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        response = self.client.get(url)
        values = (
            "Game",
            "FE%d" % kwargs['game_no'],
            "Unit",
            kwargs["name"],
            "Declines",
            "3",
        )
        for value in values:
            self.assertContains(response, value)

    def test_chapter(self):
        """
        """
        data = {"hard_mode": True, "chapter": "22"}
        kwargs = {
            "game_no": 6,
            "name": "Cath",
        }
        url = self.generate_url(**kwargs)
        response = self.client.post(url, data=data)
        self.assertEqual(VirtualMorph.objects.count(), 1)
        vmorph = VirtualMorph.objects.get()
        self.assertEqual(vmorph.owner, self.user)
        self.assertTrue(vmorph.name)
        self.assertEqual(vmorph.game_no, kwargs['game_no'])
        self.assertEqual(vmorph.unit, kwargs['name'])
        self.assertEqual(vmorph.init_options, data)
        # test for existence of init_options in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        response = self.client.get(url)
        values = (
            "Game",
            "FE%d" % kwargs['game_no'],
            "Unit",
            kwargs["name"],
            "Chapter",
            "22",
            "Difficulty",
            "Hard",
        )
        for value in values:
            self.assertContains(response, value)

    def test_lyn_mode(self):
        """
        """
        data = {"lyn_mode": True}
        kwargs = {
            "game_no": 7,
            "name": "Lyn",
        }
        url = self.generate_url(**kwargs)
        response = self.client.post(url, data=data)
        self.assertEqual(VirtualMorph.objects.count(), 1)
        vmorph = VirtualMorph.objects.get()
        self.assertEqual(vmorph.owner, self.user)
        self.assertTrue(vmorph.name)
        self.assertEqual(vmorph.game_no, kwargs['game_no'])
        self.assertEqual(vmorph.unit, kwargs['name'])
        self.assertEqual(vmorph.init_options, data)
        # test for existence of init_options in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        response = self.client.get(url)
        values = (
            "Game",
            "FE%d" % kwargs['game_no'],
            "Unit",
            kwargs["name"],
            "Campaign",
            "Tutorial",
        )
        for value in values:
            self.assertContains(response, value)

class UnitConfirmLoggedOutTests(UnitConfirmTests):
    """
    """

    def setUp(self):
        """
        """
        self.generate_url = lambda game_no, name: reverse("dracogate:unit_confirm", kwargs={"game_no": game_no, "unit": name})
        self.user = None

class LevelUpTests(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 6
        unit = "Roy"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)

    def test_level_up__virtualmorph1(self):
        """
        """
        (is_success, param_bounds) = self.vmorph.level_up(0)
        expected1 = {"min_lv": 2, "max_lv": 20}
        expected2 = False
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)

    def test_level_up__virtualmorph2(self):
        """
        """
        expected1 = {}
        expected2 = [
            ("level_up", {'num_levels': 19})
        ]
        expected3 = True
        (is_success, param_bounds) = self.vmorph.level_up(19)
        self.assertDictEqual(param_bounds, expected1)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )
        self.assertIs(is_success, expected3)

    def test_level_up__virtualmorph3(self):
        """
        """
        expected1 = {"min_lv": None, "max_lv": 20}
        expected2 = [
            ("level_up", {'num_levels': 19})
        ]
        expected3 = False
        self.vmorph.level_up(19)
        (is_success, param_bounds) = self.vmorph.level_up(1)
        self.assertDictEqual(param_bounds, expected1)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )
        self.assertIs(is_success, expected3)

    def test_level_up__formbuilder1(self):
        """
        """
        field = "target_lv"
        expected2 = 2
        expected3 = 20
        (_, param_bounds) = self.vmorph.level_up(0)
        form_class = ActionFormBuilder.level_up(param_bounds)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].min_value, expected2)
        self.assertEqual(form_class.declared_fields[field].max_value, expected3)

    def test_level_up__formbuilder3(self):
        """
        """
        field = "target_lv"
        expected2 = 20
        expected3 = 20
        expected4 = True
        # pretend Roy is at max level
        self.vmorph.level_up(19)
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.level_up(0)
        if self.vmorph.morph.current_lv == self.vmorph.morph.max_level:
            param_bounds['min_lv'] = None
        # get form class
        form_class = ActionFormBuilder.level_up(param_bounds)
        # test form class
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].min_value, expected2)
        self.assertEqual(form_class.declared_fields[field].max_value, expected3)
        self.assertIs(form_class.declared_fields[field].disabled, expected4)

    def test_level_up__forecast(self):
        """
        """
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "level_up", "stat_type": "bases", "target_lv": "20"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("33.2", "18.0")
        for value in values:
            self.assertContains(response, value)

    def test_level_up__view_post(self):
        """
        """
        expected = [["level_up", {"num_levels": 19}]]
        field = "target_lv"
        url = reverse("dracogate:level_up", kwargs={"id": self.vmorph.id})
        data = {field: 20}
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_lv, data[field])
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "level_up",
            #html.unescape(json.dumps(expected[0][1])),
            "num_levels",
            "19",
        )
        for value in values:
            self.assertContains(response, value)


class PromoteTests(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 6
        unit = "Roy"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)

    def test_promote__virtualmorph1(self):
        """
        """
        (is_success, param_bounds) = self.vmorph.promote("")
        expected1 = {"promotions": ("Master Lord",)}
        expected2 = False
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)

    def test_promote__virtualmorph2(self):
        """
        """
        promo_cls = "Master Lord"
        expected1 = {}
        expected2 = [
            ("promote", {'promo_cls': promo_cls})
        ]
        expected3 = True
        (is_success, param_bounds) = self.vmorph.promote(promo_cls)
        self.assertDictEqual(param_bounds, expected1)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )
        self.assertIs(is_success, expected3)

    def test_promote__formbuilder1(self):
        """
        """
        field = "promo_cls"
        promo_cls = "Master Lord"
        expected2 = [('', ''), (promo_cls, promo_cls)]
        (_, param_bounds) = self.vmorph.promote("")
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, expected2)

    def test_promote__formbuilder3(self):
        """
        """
        field = "promo_cls"
        expected2 = "Master Lord"
        expected4 = True
        # pretend Roy is at max level
        self.vmorph.morph.level_up(9)
        self.vmorph.morph.promote(expected2)
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.promote("")
        # get form class
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        # test form class
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, [("", "")])
        self.assertIs(form_class.declared_fields[field].disabled, expected4)

    def test_promote__forecast(self):
        """
        """
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Master Lord", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("22.0", "18.0")
        for value in values:
            self.assertContains(response, value)

    def test_promote__view_post(self):
        """
        """
        field = "promo_cls"
        promo_cls = "Master Lord"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, data[field])
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "promote",
            #html.unescape(json.dumps(expected[0][1])),
            "promo_cls",
            "Master Lord",
        )
        for value in values:
            self.assertContains(response, value)


class PromoteTests2(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 8
        unit = "Ross"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)

    def test_promote__virtualmorph1(self):
        """
        """
        self.vmorph.morph.level_up(9)
        (is_success, param_bounds) = self.vmorph.promote("")
        expected1 = {"promotions": ("Fighter", "Pirate", "Journeyman (2)")}
        expected2 = False
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)

    def test_promote__virtualmorph2(self):
        """
        """
        promo_cls = "Pirate"
        expected1 = {}
        expected2 = [
            ("promote", {'promo_cls': promo_cls})
        ]
        expected3 = True
        self.vmorph.morph.level_up(9)
        (is_success, param_bounds) = self.vmorph.promote(promo_cls)
        self.assertDictEqual(param_bounds, expected1)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )
        self.assertIs(is_success, expected3)

    def test_promote__formbuilder1(self):
        """
        Invalid promotions
        """
        field = "promo_cls"
        expected2 = [(choice, choice) for choice in ("Fighter", "Pirate", "Journeyman (2)")]
        expected2.insert(0, ("", ""))
        self.vmorph.morph.level_up(9)
        (_, param_bounds) = self.vmorph.promote("")
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, expected2)

    def test_promote__formbuilder2(self):
        """
        Level too low.
        """
        field = "promo_cls"
        expected2 = [(choice, choice) for choice in ("Fighter", "Pirate", "Journeyman (2)")]
        expected2.insert(0, ("", ""))
        (is_success, param_bounds) = self.vmorph.promote("")
        self.assertIs(is_success, False)
        self.assertIs(param_bounds['min_promo_level'], 10)
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, expected2)
        form = form_class({"promo_cls": "Pirate"})
        self.assertIs(form.is_valid(), False)
        self.assertDictEqual(form.cleaned_data, {})

    def test_promote__formbuilder3(self):
        """
        No promotions
        """
        field = "promo_cls"
        expected4 = True
        # pretend Roy is at max level
        self.vmorph.morph.level_up(9)
        self.vmorph.morph.promote(promo_cls="Journeyman (2)")
        self.vmorph.morph.level_up(9)
        self.vmorph.morph.promote(promo_cls="Journeyman (3)")
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.promote("")
        # get form class
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        # test form class
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, [("", "")])
        self.assertIs(form_class.declared_fields[field].disabled, expected4)

    def test_promote__forecast__fail(self):
        """
        """
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Pirate", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("15.0", "0.0")
        for value in values:
            self.assertContains(response, value)
        values = ("17.0",)
        for value in values:
            with self.assertRaises(AssertionError):
                self.assertContains(response, value)

    def test_promote__forecast(self):
        """
        """
        self.vmorph.morph.level_up(9)
        self.vmorph.save()
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Pirate", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("21.3", "23.3")
        for value in values:
            self.assertContains(response, value)

    def test_promote__view_post__fail(self):
        """
        """
        field = "promo_cls"
        promo_cls = "Pirate"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        values = ("10", "at least level", "Pirate")
        for value in values:
            self.assertContains(response, value)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, "Journeyman")
        self.assertListEqual(vmorph.history, [])

    def test_promote__view_post(self):
        """
        """
        self.vmorph.morph.level_up(9)
        self.vmorph.save()
        field = "promo_cls"
        promo_cls = "Pirate"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, data[field])
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "promote",
            #html.unescape(json.dumps(expected[0][1])),
            "promo_cls",
            "Pirate",
        )
        for value in values:
            self.assertContains(response, value)



class PromoteTests3(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 5
        unit = "Lara"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)
        self.vmorph.morph.level_up(9)

    def test_promote__virtualmorph1(self):
        """
        """
        (is_success, param_bounds) = self.vmorph.promote("")
        expected1 = {"promotions": ("Thief Fighter", "Dancer")}
        expected2 = False
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)

    def test_promote__virtualmorph2(self):
        """
        """
        promo_cls = "Dancer"
        expected1 = {}
        expected2 = [
            ("promote", {'promo_cls': promo_cls})
        ]
        expected3 = True
        (is_success, param_bounds) = self.vmorph.promote(promo_cls)
        self.assertDictEqual(param_bounds, expected1)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )
        self.assertIs(is_success, expected3)

    def test_promote__formbuilder1(self):
        """
        """
        field = "promo_cls"
        expected2 = [(choice, choice) for choice in ("Thief Fighter", "Dancer")]
        expected2.insert(0, ("", ""))
        (_, param_bounds) = self.vmorph.promote("")
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, expected2)

    def test_promote__formbuilder3(self):
        """
        """
        field = "promo_cls"
        expected4 = True
        # pretend Roy is at max level
        #self.vmorph.morph.level_up(9)
        self.vmorph.morph.promote(promo_cls="Dancer")
        self.vmorph.morph.level_up(9)
        self.vmorph.morph.promote(promo_cls="Thief Fighter")
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.promote("")
        # get form class
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        # test form class
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, [("", "")])
        self.assertIs(form_class.declared_fields[field].disabled, expected4)

    def test_promote__forecast__fail(self):
        """
        """
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Thief Fighter", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("14.0", "10.0")
        for value in values:
            self.assertContains(response, value)
        values = ("12.0",)
        for value in values:
            with self.assertRaises(AssertionError):
                self.assertContains(response, value)

    def test_promote__forecast(self):
        """
        """
        #self.vmorph.morph.level_up(9)
        #self.vmorph.save()
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Dancer", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("10.0", "5.0")
        for value in values:
            self.assertContains(response, value)

    def test_promote__view_post__fail(self):
        """
        """
        field = "promo_cls"
        promo_cls = "Thief Fighter"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        values = ("10", "at least level", "Thief Fighter")
        for value in values:
            self.assertContains(response, value)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, "Thief")
        self.assertListEqual(vmorph.history, [])

    def test_promote__view_post(self):
        """
        """
        self.vmorph.morph.level_up(9)
        self.vmorph.save()
        field = "promo_cls"
        promo_cls = "Dancer"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, data[field])
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "promote",
            #html.unescape(json.dumps(expected[0][1])),
            "promo_cls",
            "Dancer",
        )
        for value in values:
            self.assertContains(response, value)



class PromoteTests4(TestCase):
    """
    """

    def setUp(self):
        """
        """
        game_no = 6
        unit = "Rutger"
        init_options = {"hard_mode": False}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)

    def test_promote__virtualmorph1(self):
        """
        No errors.
        """
        promo_cls = "Swordmaster (M)"
        self.vmorph.morph.level_up(9)
        (is_success, param_bounds) = self.vmorph.promote(promo_cls)
        expected1 = {}
        expected2 = True
        expected3 = [
            ("promote", {'promo_cls': promo_cls})
        ]
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)
        self.assertListEqual(
            self.vmorph.history,
            expected3,
        )

    def test_promote__virtualmorph2(self):
        """
        Level too low.
        """
        promo_cls = "Swordmaster (M)"
        expected1 = {"min_promo_level": 10, "promotions": [promo_cls]}
        expected2 = []
        expected3 = False
        (is_success, param_bounds) = self.vmorph.promote(promo_cls)
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected3)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )

    def test_promote__virtualmorph3(self):
        """
        Invalid promotion
        """
        promo_cls = "Swordmaster (M)"
        expected1 = {"promotions": (promo_cls,)}
        expected2 = []
        expected3 = False
        self.vmorph.morph.level_up(9)
        (is_success, param_bounds) = self.vmorph.promote("")
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected3)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )

    def test_promote__virtualmorph4(self):
        """
        Level too low and invalid promotion.
        """
        promo_cls = "Swordmaster (M)"
        expected1 = {"min_promo_level": 10, "promotions": [promo_cls]}
        expected2 = []
        expected3 = False
        (is_success, param_bounds) = self.vmorph.promote("")
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected3)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )

    def test_promote__formbuilder1(self):
        """
        """
        field = "promo_cls"
        promo_cls = "Swordmaster (M)"
        expected2 = [("", ""), (promo_cls, promo_cls)]
        (_, param_bounds) = self.vmorph.promote("")
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, expected2)

    def test_promote__formbuilder3(self):
        """
        """
        field = "promo_cls"
        expected2 = "Swordmaster (M)"
        expected4 = True
        # pretend Roy is at max level
        self.vmorph.morph.level_up(9)
        self.vmorph.morph.promote(expected2)
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.promote("")
        # get form class
        form_class = ActionFormBuilder.promote(param_bounds, self.vmorph.morph)
        # test form class
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, [("", "")])
        self.assertIs(form_class.declared_fields[field].disabled, expected4)

    def test_promote__forecast__fail(self):
        """
        """
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Swordmaster (M)", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        values = ("22.0", "13.0")
        for value in values:
            self.assertContains(response, value)
        values = ("27.0",)
        for value in values:
            with self.assertRaises(AssertionError):
                self.assertContains(response, value)

    def test_promote__forecast(self):
        """
        """
        self.vmorph.morph.level_up(16)
        self.vmorph.save()
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "promote", "promo_cls": "Swordmaster (M)", "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("34.8", "39.8")
        for value in values:
            self.assertContains(response, value)

    def test_promote__view_post__fail(self):
        """
        """
        field = "promo_cls"
        promo_cls = "Swordmaster (M)"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        values = ("10", "at least level", "Swordmaster (M)")
        for value in values:
            self.assertContains(response, value)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, "Myrmidon")
        self.assertListEqual(vmorph.history, [])

    def test_promote__view_post(self):
        """
        """
        self.vmorph.morph.level_up(9)
        self.vmorph.save()
        field = "promo_cls"
        promo_cls = "Swordmaster (M)"
        expected = [["promote", {"promo_cls": promo_cls}]]
        url = reverse("dracogate:promote", kwargs={"id": self.vmorph.id})
        data = {field: promo_cls}
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_cls, data[field])
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "promote",
            #html.unescape(json.dumps(expected[0][1])),
            "promo_cls",
            "Swordmaster (M)",
        )
        for value in values:
            self.assertContains(response, value)

class UseStatBoosterTests(TestCase):
    """
    """

    # https://serenesforest.net/binding-blade/characters/average-stats/hard-mode/rutger/
    def setUp(self):
        """
        """
        game_no = 6
        unit = "Rutger"
        init_options = {"hard_mode": True}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)
        self.vmorph.morph.level_up(20 - self.vmorph.morph.current_lv)
        #print(self.vmorph.morph._miscellany)
        self.vmorph.save()

    def test_use_stat_booster__virtualmorph1(self):
        """
        No errors.
        """
        item_name = "Energy Ring"
        (is_success, param_bounds) = self.vmorph.use_stat_booster(item_name)
        expected1 = {}
        expected2 = True
        expected3 = [
            ("use_stat_booster", {'item_name': item_name})
        ]
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)
        self.assertListEqual(
            self.vmorph.history,
            expected3,
        )

    def test_use_stat_booster__virtualmorph2(self):
        """
        Stat is maxed.
        """
        item_name = "Speedwings"
        expected2 = []
        expected3 = False
        (is_success, param_bounds) = self.vmorph.use_stat_booster(item_name)
        self.assertIsNone(param_bounds)
        self.assertIs(is_success, expected3)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )

    def test_use_stat_booster__formbuilder1(self):
        """
        """
        field = "item_name"
        item_name = "Energy Ring"
        expected2 = [(choice, choice) for choice in (
            "",
            "Angelic Robe",
            "Energy Ring",
            "Secret Book",
            "Speedwings",
            "Goddess Icon",
            "Dragonshield",
            "Talisman",
            "Boots",
            "Body Ring",
        )]
        (_, param_bounds) = self.vmorph.use_stat_booster("")
        form_class = ActionFormBuilder.use_stat_booster(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)
        self.assertEqual(form_class.declared_fields[field].choices, expected2)

    def test_use_stat_booster__formbuilder2(self):
        """
        Check validation.
        """
        field = "item_name"
        item_name = "Speedwings"
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.use_stat_booster("")
        # get form class
        form_class = ActionFormBuilder.use_stat_booster(param_bounds, self.vmorph.morph)
        form = form_class({"item_name": "Speedwings"})
        self.assertIs(form.is_valid(), False)

    def test_use_stat_booster__forecast__fail(self):
        """
        """
        field = "item_name"
        value = "Speedwings"
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "use_stat_booster", field: value, "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("20.0", "38.3")
        for value in values:
            self.assertContains(response, value)
        values = ("22.0",)
        for value in values:
            with self.assertRaises(AssertionError):
                self.assertContains(response, value)

    def test_use_stat_booster__forecast(self):
        """
        """
        field = "item_name"
        value = "Angelic Robe"
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "use_stat_booster", field: value, "stat_type": "bases"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("45.3", "38.3")
        for value in values:
            self.assertContains(response, value)

    def test_use_stat_booster__view_post__fail(self):
        """
        """
        field = "item_name"
        value = "Speedwings"
        expected = [["use_stat_booster", {field: value}]]
        url = reverse("dracogate:use_stat_booster", kwargs={"id": self.vmorph.id})
        data = {field: value}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        values = ("cannot use", "Speedwings", "Spd", "is maxed")
        for value in values:
            self.assertContains(response, value)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_stats.Spd, 20_00)
        self.assertListEqual(vmorph.history, [])

    def test_use_stat_booster__view_post(self):
        """
        """
        #self.vmorph.morph.level_up(9)
        #self.vmorph.save()
        field = "item_name"
        value = "Angelic Robe"
        expected = [["use_stat_booster", {field: value}]]
        url = reverse("dracogate:use_stat_booster", kwargs={"id": self.vmorph.id})
        data = {field: value}
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.current_stats.HP, 45_30)
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "use_stat_booster",
            #html.unescape(json.dumps(expected[0][1])),
            "item_name",
            "Angelic Robe",
        )
        for value in values:
            self.assertContains(response, value)


class UseStatBoosterTests2(TestCase):
    """
    """

    # https://serenesforest.net/binding-blade/characters/average-stats/hard-mode/rutger/
    def setUp(self):
        """
        """
        game_no = 4
        unit = "Sigurd"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)

    def test_use_stat_booster__virtualmorph(self):
        """
        Not implemented
        """
        with self.assertRaises(NotImplementedError) as e:
            self.vmorph.use_stat_booster("")

    def test_use_stat_booster__formbuilder1(self):
        """
        """
        field = "item_name"
        item_name = "Energy Ring"
        param_bounds = {"stat_boosters": (
            "",
            "Angelic Robe",
            "Energy Ring",
            "Secret Book",
            "Speedwings",
            "Goddess Icon",
            "Dragonshield",
            "Talisman",
            "Boots",
            "Body Ring",
        )}
        form_class = ActionFormBuilder.use_stat_booster(param_bounds, self.vmorph.morph)
        form = form_class({field: item_name})
        with self.assertRaises(TypeError):
            form.is_valid()

    def test_use_stat_booster__view_post__fail(self):
        """
        """
        field = "item_name"
        value = "Speedwings"
        expected = [["use_stat_booster", {field: value}]]
        url = reverse("dracogate:use_stat_booster", kwargs={"id": self.vmorph.id})
        data = {field: value}
        with self.assertRaises(NotImplementedError):
            self.client.post(url, data=data)


class UseAfasDropsTests(TestCase):
    """
    """

    # https://serenesforest.net/blazing-sword/characters/average-stats/nino/
    def setUp(self):
        """
        """
        game_no = 7
        unit = "Nino"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)
        #self.vmorph.morph.level_up(20 - self.vmorph.morph.current_lv)
        #print(self.vmorph.morph._miscellany)
        #self.vmorph.save()

    def test_use_afas_drops__virtualmorph1(self):
        """
        No errors.
        """
        (is_success, param_bounds) = self.vmorph.use_afas_drops(True)
        expected1 = {}
        expected2 = True
        expected3 = [
            ("use_afas_drops", {})
        ]
        self.assertDictEqual(param_bounds, expected1)
        self.assertIs(is_success, expected2)
        self.assertListEqual(
            self.vmorph.history,
            expected3,
        )

    def test_use_afas_drops__virtualmorph2(self):
        """
        Afa's Drops is used already.
        """
        expected2 = []
        expected3 = False
        self.vmorph.morph.use_afas_drops()
        (is_success, param_bounds) = self.vmorph.use_afas_drops(True)
        self.assertIsNone(param_bounds)
        self.assertIs(is_success, expected3)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )

    def test_use_afas_drops__virtualmorph3(self):
        """
        Refuse to use Afa's Drops.
        """
        expected2 = []
        expected3 = False
        self.vmorph.morph.use_afas_drops()
        (is_success, param_bounds) = self.vmorph.use_afas_drops(False)
        self.assertDictEqual(param_bounds, {})
        self.assertIs(is_success, expected3)
        self.assertListEqual(
            self.vmorph.history,
            expected2,
        )

    def test_use_afas_drops__formbuilder1(self):
        """
        """
        field = "to_consume"
        (_, param_bounds) = self.vmorph.use_afas_drops(False)
        form_class = ActionFormBuilder.use_afas_drops(param_bounds, self.vmorph.morph)
        self.assertIn(field, form_class.declared_fields)

    def test_use_afas_drops__formbuilder2(self):
        """
        Check validation.
        """
        field = "to_consume"
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.use_afas_drops(False)
        # get form class
        self.vmorph.morph.use_afas_drops()
        form_class = ActionFormBuilder.use_afas_drops(param_bounds, self.vmorph.morph)
        form = form_class({"to_consume": True})
        self.assertIs(form.is_valid(), False)

    def test_use_afas_drops__formbuilder2(self):
        """
        Check validation.
        """
        field = "to_consume"
        # try to get param_bounds
        (_, param_bounds) = self.vmorph.use_afas_drops(False)
        # get form class
        form_class = ActionFormBuilder.use_afas_drops(param_bounds, self.vmorph.morph)
        form = form_class({"to_consume": False})
        self.assertIs(form.is_valid(), False)

    def test_use_afas_drops__forecast(self):
        """
        """
        field = "to_consume"
        value = "True"
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "use_afas_drops", field: value, "stat_type": "growths"}
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("20", "15")
        for value in values:
            self.assertContains(response, value)
        # TODO: with self.assertRaises(...): self.assertContains for ...forecast__fail methods
        # NOTE: Technically proves nothing, just the presence of the before-values.

    def test_use_afas_drops__forecast__fail(self):
        """
        """
        field = "to_consume"
        value = "False"
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "use_afas_drops", "stat_type": "growths"}
        self.vmorph.morph.use_afas_drops()
        self.vmorph.save()
        #print(self.vmorph.morph._miscellany is not None)
        #print(self.vmorph.morph.growth_rates.as_dict())
        response = self.client.get(url, query_params=query_params)
        # HP values
        values = ("20", "50")
        for value in values:
            self.assertContains(response, value)
        values = ("15", "45")
        for value in values:
            with self.assertRaises(AssertionError):
                self.assertContains(response, value)

    def test_use_afas_drops__view_post__fail(self):
        """
        Already used Afa's Drops.
        """
        field = "to_consume"
        value = "True"
        expected = [["use_afas_drops", {}]]
        url = reverse("dracogate:use_afas_drops", kwargs={"id": self.vmorph.id})
        data = {field: value}
        self.vmorph.morph.use_afas_drops()
        self.vmorph.save()
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        #values = ("Afa", "Drops", "already used", self.vmorph.morph.name)
        # NOTE: Because upon using Afa's Drops, the checkbox is disabled initially, and the form containing it is submitted, resulting in the error message.
        #values = ("make", "selection")
        #for value in values:
            #self.assertContains(response, value)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.growth_rates.Def, 20)
        self.assertListEqual(vmorph.history, [])

    def test_use_afas_drops__view_post__fail2(self):
        """
        Did not use Afa's Drops.
        """
        field = "to_consume"
        value = "False"
        morph = self.vmorph.morph
        expected = [["use_afas_drops", {}]]
        url = reverse("dracogate:use_afas_drops", kwargs={"id": self.vmorph.id})
        data = {}
        self.assertEqual(morph.growth_rates.Def, 15)
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        #values = ("make", "selection")
        #for value in values:
            #self.assertContains(response, value)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.growth_rates.Def, 15)
        self.assertListEqual(vmorph.history, [])

    def test_use_afas_drops__view_post(self):
        """
        """
        #self.vmorph.morph.level_up(9)
        #self.vmorph.save()
        morph = self.vmorph.morph
        field = "to_consume"
        value = "True"
        expected = [["use_afas_drops", {}]]
        url = reverse("dracogate:use_afas_drops", kwargs={"id": self.vmorph.id})
        data = {field: value}
        self.assertEqual(morph.growth_rates.Def, 15)
        response = self.client.post(url, data=data)
        self.assertLess(response.status_code, 400)
        vmorph = VirtualMorph.objects.get(id=self.vmorph.id)
        morph = vmorph.init()
        self.assertEqual(morph.growth_rates.Def, 20)
        self.assertListEqual(vmorph.history, expected)
        # test for existence of actions in morph_detail
        url = reverse("dracogate:morph_detail", kwargs={"id": vmorph.id})
        self.assertRedirects(response, url)
        response = self.client.get(url)
        values = (
            "use_afas_drops",
            #html.unescape(json.dumps(expected[0][1])),
            "{}",
        )
        for value in values:
            self.assertContains(response, value)


class UseAfasDropsTests2(TestCase):
    """
    """

    # https://serenesforest.net/blazing-sword/characters/average-stats/nino/
    def setUp(self):
        """
        """
        game_no = 6
        unit = "Roy"
        init_options = {}
        self.user = User.objects.create()
        self.vmorph = VirtualMorph.objects.create(
            owner=self.user,
            game_no=game_no,
            unit=unit,
            init_options=init_options,
        )
        self.vmorph.morph = get_morph(game_no, unit, **init_options)
        #self.vmorph.morph.level_up(20 - self.vmorph.morph.current_lv)
        #print(self.vmorph.morph._miscellany)
        #self.vmorph.save()

    def test_use_afas_drops__virtualmorph1(self):
        """
        """
        with self.assertRaises(AttributeError):
            self.vmorph.use_afas_drops(True)

    def test_use_afas_drops__formbuilder1(self):
        """
        """
        field = "to_consume"
        param_bounds = {}
        with self.assertRaises(KeyError): 
            ActionFormBuilder.use_afas_drops(param_bounds, self.vmorph.morph)

    def test_use_afas_drops__forecast(self):
        """
        """
        field = "to_consume"
        value = "True"
        url = reverse("dracogate:action_forecast", kwargs={"id": self.vmorph.id})
        query_params = {"action": "use_afas_drops", field: value, "stat_type": "growths"}
        with self.assertRaises(AttributeError):
            self.client.get(url, query_params=query_params)
        # TODO: with self.assertRaises(...): self.assertContains for ...forecast__fail methods
        # NOTE: Technically proves nothing, just the presence of the before-values.

    def test_use_afas_drops__view_post(self):
        """
        """
        #self.vmorph.morph.level_up(9)
        #self.vmorph.save()
        morph = self.vmorph.morph
        field = "to_consume"
        value = "True"
        expected = [["use_afas_drops", {}]]
        url = reverse("dracogate:use_afas_drops", kwargs={"id": self.vmorph.id})
        data = {field: value}
        with self.assertRaises(KeyError):
            self.client.post(url, data=data)

