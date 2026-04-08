"""
"""

import abc
from typing import (
    List,
    Any,
)

from django import forms

FATHERS = (
    'Arden',
    'Azel',
    'Alec',
    'Claude',
    'Jamka',
    'Dew',
    'Noish',
    'Fin',
    'Beowolf',
    'Holyn',
    'Midayle',
    'Levin',
    'Lex',
)

class Options:
    """
    """

    def father(values: List[str]):
        """
        """
        return forms.ChoiceField(
            initial=values[0],
            #max_length=9,
            #required=False,
            choices=[(father, father) for father in values],
        )

    def hard_mode(values: List[bool]):
        """
        """
        return forms.BooleanField(
            initial=values[0],
            #required=False,
        )

    def number_of_declines(values: List[int]):
        """
        """
        return forms.IntegerField(
            initial=values[0],
            min_value=0,
            max_value=3,
            step_size=1,
            #required=False,
        )

    def chapter(values: List[str]):
        """
        """
        return forms.ChoiceField(
            choices=[(chapter, chapter) for chapter in values],
            #required=False,
        )

    def lyn_mode(values: List[bool]):
        """
        """
        return forms.BooleanField(
            initial=values[0],
            #required=False,
        )

class InitFormBuilder:
    """
    """

    def build_form_class(game_no_: int, name_: str, init_params: dict[str, List[bool | str | int]]):
        """
        """
        class InitForm(forms.Form):
            """
            """
            game_no = forms.IntegerField(
                initial=game_no_,
                min_value=4,
                max_value=9,
                step_size=1,
                widget=forms.HiddenInput(),
            )
            name = forms.CharField(
                initial=name_,
                max_length=9,
                widget=forms.HiddenInput(),
            )
        for field_name, values in init_params.items():
            InitForm.base_fields[field_name] = getattr(Options, field_name)(values)
        return InitForm

    class BaseForm(forms.Form):
        """
        """
        game_no = forms.IntegerField(
            min_value=4,
            max_value=9,
            step_size=1,
            widget=forms.HiddenInput(),
        )
        name = forms.CharField(
            max_length=9,
            widget=forms.HiddenInput(),
        )

    class Form4(BaseForm):
        """
        """
        father = forms.CharField(
            max_length=9,
            required=False,
        )

    class Form5(BaseForm):
        """
        """

    class Form6(BaseForm):
        """
        """
        hard_mode = forms.BooleanField(
            initial=False,
            required=False,
        )
        number_of_declines = forms.IntegerField(
            initial=0,
            min_value=0,
            max_value=3,
            step_size=1,
            required=False,
        )
        chapter = forms.ChoiceField(
            required=False,
        )

    class Form7(BaseForm):
        """
        """
        lyn_mode = forms.BooleanField(
            initial=False,
            required=False,
        )
        hard_mode = forms.BooleanField(
            initial=False,
            required=False,
        )

    class Form8(BaseForm):
        """
        """

    class Form9(BaseForm):
        """
        """

