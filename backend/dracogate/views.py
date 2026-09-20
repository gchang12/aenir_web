"""
"""

from django.views.generic import base, edit

from aenir.games import FireEmblemGame
from aenir import InitError
from aenir.morph import get_morph, get_morph_class

from . import models
from . import forms

def get_temp_morph(game_no, unit, init_options):
    """
    """
    option_fields = forms.InitFormBuilder.OPTION_FIELDS()
    init_options = dict(
        map(
            lambda key_value: (
                key_value if key_value[0] not in ("lyn_mode", "hard_mode")
                else (key_value[0], (True if key_value[1] == "True" else False))
            ),
            filter(
                lambda key_value: key_value[0] in option_fields,
                init_options.items(),
            )
        )
    )
    #print("init_options", init_options)
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
    #model = models.VirtualMorph
    #fields = []

    def get_context_data(self):
        """
        """
        context = super().get_context_data(**self.kwargs)
        context.update(self.kwargs)
        return context

    def get_form_class(self):
        """
        """
        #self.init_params = {}
        #form = super().get_form_class()
        form_class = forms.InitFormBuilder.build_form_class(self.init_params)
        return form_class

    def get(self, request, game_no, unit):
        """
        """
        (init_params, _) = get_temp_morph(game_no, unit, request.GET.dict())
        self.init_params = init_params
        return super().get(request, game_no, unit)

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
        context['stats'] = models.StatsBundler.init_forecast(morph)
        context['unit_level'] = morph.current_lv
        context['unit_class'] = morph.current_cls
        #print(context)
        return context

