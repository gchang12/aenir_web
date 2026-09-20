"""
"""

from django import forms

class InitFormBuilder:
    """
    """

    @staticmethod
    def OPTION_FIELDS():
        return (
            "father",
            "hard_mode",
            "number_of_declines",
            "chapter",
            "lyn_mode",
        )

    @staticmethod
    def father(choices):
        """
        """
        return forms.ChoiceField(
            choices=[(choice, choice) for choice in choices],
            required=True,
            initial=choices[0],
            label="Father",
        )

    @staticmethod
    def hard_mode(choices):
        """
        """
        return forms.NullBooleanField(
            required=True,
            initial=choices[0],
            label="Hard Mode",
            widget=forms.Select(
                choices=((choice, choice) for choice in choices),
            ),
        )

    @staticmethod
    def number_of_declines(choices):
        """
        """
        return forms.IntegerField(
            min_value=choices[0],
            max_value=choices[-1],
            step_size=1,
            required=True,
            initial=choices[0],
            label="Number of Declines",
        )

    @staticmethod
    def chapter(choices):
        """
        """
        return forms.ChoiceField(
            choices=[(choice, choice) for choice in choices],
            required=True,
            initial=choices[0],
            label="Chapter",
        )

    @staticmethod
    def lyn_mode(choices):
        """
        """
        return forms.NullBooleanField(
            required=True,
            initial=choices[0],
            label="Lyn Mode",
            widget=forms.Select(
                choices=((choice, choice) for choice in choices),
            ),
        )

    @classmethod
    def build_form_class(cls, init_params):
        """
        """
        class InitOptionsForm(forms.Form):
            """
            """
        for init_param, choices in init_params.items():
            InitOptionsForm.declared_fields[init_param] = getattr(cls, init_param)(choices)
        return InitOptionsForm

'''
    def __init__(self, name: str, *, father: str | None = None):
    def __init__(self, name: str):
    def __init__(self, name: str, *, hard_mode: bool | None = None, number_of_declines: int | None = None, chapter: str | None = None):
    def __init__(self, name: str, *, lyn_mode: bool | None = None, hard_mode: bool | None = None):
    def __init__(self, name: str):
    def __init__(self, name: str):
'''
