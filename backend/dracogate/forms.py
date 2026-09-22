"""
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from aenir import PromotionError

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

class ActionFormBuilder:
    """
    """

    @staticmethod
    def level_up(param_bounds):
        """
        """
        #print(param_bounds)
        class LevelUpForm(forms.Form):
            """
            """
            target_lv = forms.IntegerField(
                #initial=initial,
                min_value=param_bounds['min_lv'] or param_bounds['max_lv'],
                max_value=param_bounds['max_lv'],
                step_size=1,
                disabled=param_bounds['min_lv'] is None,
                label="Target Level",
            )

        return LevelUpForm

    @staticmethod
    def promote(param_bounds, morph):
        """
        """
        choices = ([] if param_bounds is None else [(choice, choice) for choice in param_bounds["promotions"]])

        class PromotionClassField(forms.ChoiceField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                try:
                    morph.promote(promo_cls=value)
                except PromotionError as e:
                    if e.reason == e.Reason.LEVEL_TOO_LOW:
                        raise ValidationError(
                            _("%(name)s has to be at least level %(min_promo_level)d to promote to '%(value)s'."),
                            params={"min_promo_level": morph.min_promo_level, "value": value, "name": morph.name},
                        )
                return True

        class PromoteForm(forms.Form):
            """
            """
            promo_cls = PromotionClassField(
                initial="",
                choices=choices,
                required=True,
                label="Promotion",
                disabled=param_bounds is None,
            )
        return PromoteForm

'''
    def __init__(self, name: str, *, father: str | None = None):
    def __init__(self, name: str):
    def __init__(self, name: str, *, hard_mode: bool | None = None, number_of_declines: int | None = None, chapter: str | None = None):
    def __init__(self, name: str, *, lyn_mode: bool | None = None, hard_mode: bool | None = None):
    def __init__(self, name: str):
    def __init__(self, name: str):
'''
