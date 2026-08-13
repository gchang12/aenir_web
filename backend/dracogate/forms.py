"""
Dynamic forms for previewing Morph stats given some state.
"""

import abc
from typing import (
    List,
    Any,
)

from django import forms

class InitFormBuilder:
    """
    Container for all classes and the like for initializing a unit.
    """

    class Options:
        """
        Container for option fields to be rendered in a form.
        """

        def father(values: List[str]):
            """
            Lists FE4 fathers.
            """
            return forms.ChoiceField(
                initial=values[0],
                choices=[(father, father) for father in values],
                required=True,
            )

        def hard_mode(values: List[bool]):
            """
            Lists values for 'hard_mode' option.
            """
            return forms.BooleanField(
                initial=values[0],
                required=False,
                label="Hard Mode",
            )

        def number_of_declines(values: List[int]):
            """
            Lists values for 'number_of_declines' option.
            """
            return forms.IntegerField(
                initial=values[0],
                min_value=0,
                max_value=3,
                step_size=1,
                required=True,
                label="Number of Declines",
            )

        def chapter(values: List[str]):
            """
            Lists values for 'chapter' option depending on unit.
            """
            return forms.ChoiceField(
                choices=[(chapter, chapter) for chapter in values],
                initial=values[0],
                required=True,
            )

        def lyn_mode(values: List[bool]):
            """
            Lists values for 'lyn_mode' option.
            """
            return forms.BooleanField(
                initial=values[0],
                required=False,
                label="Lyn Mode",
            )

    @classmethod
    def build_form_class(cls, game_no_: int, name_: str, init_params: dict[str, List[bool | str | int]]):
        """
        Builds form class for initializing a unit.
        """
        class InitForm(forms.Form):
            """
            Prompts user to respond with 'game_no', 'name', and option values if applicable.
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

# TODO: Implement
class LevelUpFormBuilder:
    """
    """
