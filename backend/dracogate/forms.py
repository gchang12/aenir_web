"""
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from aenir import (
    PromotionError,
    StatBoosterError,
    GrowthsItemError,
    ScrollError,
)

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
        choices = [(False, "Hard"), (True, "Normal")]
        return forms.NullBooleanField(
            required=True,
            initial=False,
            label="Difficulty",
            widget=forms.Select(
                choices=choices,
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
        choices = [(False, "Eliwood/Hector"), (True, "Lyn")]
        return forms.NullBooleanField(
            required=True,
            initial=False,
            label="Mode",
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
        choices.insert(0, ("", ""))

        class PromotionClassField(forms.ChoiceField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                try:
                    #print("PromotionClassField")
                    morph.copy().promote(promo_cls=value)
                except PromotionError as e:
                    if e.reason == e.Reason.LEVEL_TOO_LOW:
                        raise ValidationError(
                            _("%(name)s has to be at least level %(min_promo_level)d to promote to '%(value)s'."),
                            params={"min_promo_level": morph.min_promo_level, "value": value, "name": morph.name},
                            code="LEVEL_TOO_LOW",
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

    @staticmethod
    def use_stat_booster(param_bounds, morph):
        """
        """
        choices = [(choice, choice) for choice in param_bounds["stat_boosters"]]
        choices.insert(0, ("", ""))

        class StatBoosterField(forms.ChoiceField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                (stat_name, _bonus) = morph.stat_boosters[value]
                try:
                    morph.copy().use_stat_booster(item_name=value)
                except StatBoosterError as e:
                    if e.reason == e.Reason.STAT_IS_MAXED:
                        raise ValidationError(
                            _("%(name)s cannot use %(item_name)s. %(stat_name)s is maxed."),
                            params={"item_name": value, "name": morph.name, "stat_name": stat_name},
                            code="STAT_IS_MAXED",
                        )
                return True

        class UseStatBoosterForm(forms.Form):
            """
            """
            item_name = StatBoosterField(
                initial="",
                choices=choices,
                required=True,
                label="Stat Booster",
            )
        return UseStatBoosterForm

    @staticmethod
    def use_afas_drops(param_bounds, morph):
        """
        """
        #choices = [('', ''), ('on', 'on')]
        #choices.insert(0, ("", ""))
        choices = (False, True)

        class ToConsumeField(forms.NullBooleanField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                if value is True:
                    try:
                        morph.copy().use_afas_drops()
                    except GrowthsItemError:
                        raise ValidationError(
                            _("%(name)s has already used Afa's Drops."),
                            params={"name": morph.name},
                            code="ALREADY_CONSUMED",
                        )
                elif value in (None, False):
                    raise ValidationError(
                        _("Please select 'True' to use your Afa's Drops."),
                        params={"name": morph.name},
                        code="no_selection",
                    )
                return True

        class UseAfasDropsForm(forms.Form):
            """
            """
            to_consume = ToConsumeField(
                initial=False,
                required=True,
                disabled=morph._miscellany["Afa's Drops"] is not None,
                label="Use Afa's Drops",
                widget=forms.Select(
                    choices=[(choice, choice) for choice in choices],
                ),
            )
        return UseAfasDropsForm

    @staticmethod
    def set_scrolls(param_bounds, morph):
        """
        """
        choices = [(choice, choice) for choice in param_bounds["scrolls"]]

        class ScrollsField(forms.MultipleChoiceField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                try:
                    morph.copy().set_scrolls(scrolls=value)
                except ScrollError as e:
                    if e.reason == e.Reason.NO_INVENTORY_SPACE:
                        actual_list_len = len(value)
                        raise ValidationError(
                            _("Too many scrolls selected (%(actual_list_len)d). Max: %(max_list_len)d."),
                            params={"actual_list_len": actual_list_len, "max_list_len": morph.inventory_size},
                            code="NO_INVENTORY_SPACE",
                        )
                return True

        class SetScrollsForm(forms.Form):
            """
            """
            scrolls = ScrollsField(
                choices=choices,
                required=True,
                label="Scrolls",
            )
        return SetScrollsForm

    @staticmethod
    def shapeshift(param_bounds, morph):
        """
        """
        cls_to_transform_to = morph._miscellany["cls_to_transform_to"]
        current_cls = morph.current_cls
        choices = [(False, current_cls), (True, cls_to_transform_to)]

        class ToShapeshiftField(forms.NullBooleanField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                if morph.is_laguz is False:
                    raise ValidationError(
                        _("%(name)s is not a laguz and cannot shapeshift."),
                        params={"name": morph.name},
                        code="not_a_laguz",
                    )
                if value in (None, False):
                    raise ValidationError(
                        _("%(name)s is currently a %(current_cls)s. Please select '%(cls_to_transform_to)s' to shapeshift."),
                        params={"name": morph.name, "current_cls": current_cls, "cls_to_transform_to": cls_to_transform_to},
                        code="no_selection",
                    )
                return True

        class ShapeshiftForm(forms.Form):
            """
            """
            to_shapeshift = ToShapeshiftField(
                initial=False,
                required=True,
                disabled=morph.is_laguz is False,
                label="Shapeshift",
                widget=forms.Select(
                    choices=choices,
                ),
            )

        return ShapeshiftForm

    @staticmethod
    def use_metiss_tome(param_bounds, morph):
        """
        """
        #choices = [('', ''), ('on', 'on')]
        #choices.insert(0, ("", ""))
        choices = (False, True)

        class ToConsumeField(forms.NullBooleanField):
            """
            """

            def validate(self, value):
                """
                """
                super().validate(value)
                if value is True:
                    try:
                        morph.copy().use_metiss_tome()
                    except GrowthsItemError:
                        raise ValidationError(
                            _("%(name)s has already used Metis's Tome."),
                            params={"name": morph.name},
                            code="ALREADY_CONSUMED",
                        )
                elif value in (None, False):
                    raise ValidationError(
                        _("Please select 'True' to use your Metis's Tome."),
                        params={"name": morph.name},
                        code="no_selection",
                    )
                return True

        class UseAfasDropsForm(forms.Form):
            """
            """
            to_consume = ToConsumeField(
                initial=False,
                required=True,
                disabled=morph._miscellany["Metis's Tome"] is not None,
                label="Use Metis's Tome",
                widget=forms.Select(
                    choices=[(choice, choice) for choice in choices],
                ),
            )
        return UseAfasDropsForm


'''
    def __init__(self, name: str, *, father: str | None = None):
    def __init__(self, name: str):
    def __init__(self, name: str, *, hard_mode: bool | None = None, number_of_declines: int | None = None, chapter: str | None = None):
    def __init__(self, name: str, *, lyn_mode: bool | None = None, hard_mode: bool | None = None):
    def __init__(self, name: str):
    def __init__(self, name: str):
'''
