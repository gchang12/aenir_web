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

class InitFormBuilder:
    """
    """

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

    @classmethod
    def build_form_class(cls, game_no_: int, name_: str, init_params: dict[str, List[bool | str | int]]):
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
            InitForm.base_fields[field_name] = getattr(cls.Options, field_name)(values)
        return InitForm
