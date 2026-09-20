"""
"""

from django.test import TestCase
import django.forms
from django.urls import reverse
from django.contrib.auth import get_user_model

from aenir import (
    get_morph,
    InitError,
)

from dracogate.forms import (
    InitFormBuilder,
    LevelUpFormBuilder,
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
        form_class = LevelUpFormBuilder.build_form_class(param_bounds)
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
        form_class = LevelUpFormBuilder.build_form_class(param_bounds)
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

