"""
"""

from django.views.generic import base, edit
from django.urls import reverse_lazy

from aenir.games import FireEmblemGame
from aenir import InitError
from aenir.morph import get_morph, get_morph_class

from dracogate.models import (
    VirtualMorph,
    StatsBundler,
)
from . import forms

def parse_init_option(init_option):
    """
    """
    key, value = init_option
    if key in ("lyn_mode", "hard_mode"):
        value = {
            "True": True,
            "False": False,
        }[value]
    elif key == "number_of_declines":
        value = int(value)
    return key, value

def clean_init_options(init_options):
    """
    """
    option_fields = forms.InitFormBuilder.OPTION_FIELDS()
    init_options = dict(
        map(
            parse_init_option,
            filter(
                lambda key_value: key_value[0] in option_fields,
                init_options.items(),
            )
        )
    )
    return init_options

def get_temp_morph(game_no, unit, init_options):
    """
    """
    init_options = clean_init_options(init_options)
    try:
        temp_morph = get_morph(game_no, unit, **init_options)
        init_params = {}
    except InitError as e:
        init_params = e.init_params
        init_options.update({key: value[0] for key, value in init_params.items()})
        temp_morph = get_morph(game_no, unit, **init_options)
    return (init_params, temp_morph)

class GameSelectView(base.TemplateView):
    """
    """
    template_name = "dracogate/game_select.html"

    def get_context_data(self):
        """
        """
        context = super().get_context_data()
        context['games'] = [
            {
                "title": fe_game.formal_name,
                "game_no": fe_game.value,
            } for fe_game in FireEmblemGame
        ]
        return context

class UnitSelectView(base.TemplateView):
    """
    """
    template_name = "dracogate/unit_select.html"

    def get_context_data(self, game_no):
        """
        """
        context = super().get_context_data()
        context['units'] = get_morph_class(game_no).CHARACTERS()
        context['game_no'] = game_no
        return context

# TODO: Figure out how to implement these

class UnitConfirmView(edit.FormView):
    """
    """
    template_name = "dracogate/unit_confirm.html"
    success_url = reverse_lazy("dracogate:morph_select")

    def get_context_data(self):
        """
        """
        #print("get_context_data", self.kwargs)
        context = super().get_context_data(**self.kwargs)
        context.update(self.kwargs)
        return context

    def get_form_class(self):
        """
        """
        #self.init_params = {}
        #form = super().get_form_class()
        #print(self.init_params)
        form_class = forms.InitFormBuilder.build_form_class(self.init_params)
        #print(form_class.declared_fields)
        #print("get_form_class", form_class.declared_fields)
        return form_class

    def get(self, request, game_no, unit):
        """
        """
        (init_params, _) = get_temp_morph(game_no, unit, request.GET.dict())
        self.init_params = init_params
        self.route_params = {
            "game_no": game_no,
            "unit": unit,
        }
        return super().get(request, game_no, unit)

    def post(self, request, game_no, unit):
        """
        """
        (init_params, _) = get_temp_morph(game_no, unit, {})
        self.init_params = init_params
        self.route_params = {
            "game_no": game_no,
            "unit": unit,
        }
        #print("post", self.init_params)
        return super().post(request, game_no, unit)

    def form_valid(self, form):
        """
        """
        #print("form_valid", form.is_valid())
        #print("form_valid", form.declared_fields)
        #print("form_valid", form.cleaned_data)
        #print("form_valid", self.route_params)
        vmorph = VirtualMorph(
            owner=(self.request.user if self.request.user.is_authenticated else None),
            game_no=self.route_params.pop("game_no"),
            unit=self.route_params.pop("unit"),
            init_options=form.cleaned_data,
        )
        vmorph.save()
        return super().form_valid(form)

class UnitConfirmForecast(base.TemplateView):
    """
    """
    template_name = "dracogate/unit_confirm_forecast.html"

    def get_context_data(self, game_no, unit):
        """
        """
        # get stats
        query_params = self.request.GET.dict()
        context = super().get_context_data()
        #print(query_params)
        (init_params, morph) = get_temp_morph(game_no, unit, query_params)
        context['stats'] = StatsBundler.init_forecast(morph)
        context['unit_level'] = morph.current_lv
        context['unit_class'] = morph.current_cls
        #print(context)
        return context

class MorphSelectView(base.TemplateView):
    """
    """
    template_name = "dracogate/morph_select.html"

