"""
"""

from django.shortcuts import render
from django.views.generic.base import TemplateView

import aenir.morph
import aenir.games
# TODO: Import all exceptions into 'aenir' for semantics' sake.
from aenir import get_morph
from aenir._exceptions import (
    InitError,
)

from .models import VirtualMorph

class GameSelectView(TemplateView):
    """
    """
    template_name = "dracogate/game_select.html"

    def get_context_data(self, **kwargs):
        """
        """
        context = super().get_context_data(**kwargs)
        games = {game.value: game.formal_name for game in aenir.games.FireEmblemGame}
        context['games'] = games
        return context

class UnitSelectView(GameSelectView):
    """
    """
    template_name = "dracogate/unit_select.html"

    def get_context_data(self, game_no, **kwargs):
        """
        """
        context = super().get_context_data(**kwargs)
        morph_cls = getattr(aenir.morph, "Morph%d" % game_no)
        units = morph_cls.get_true_character_list()
        context['route_params'] = {}
        context['route_params']['game_no'] = game_no
        context['units'] = units
        return context

class UnitConfirmView(UnitSelectView, FormView):
    """
    """
    template_name = "dracogate/unit_confirm.html"

    def get_context_data(self, game_no, name, **kwargs):
        """
        """
        context = super().get_context_data(game_no, **kwargs)
        # TODO: namespace names by prefixing them with 'route_params' as appropriate
        context['route_params']['name'] = name
        try:
            morph = get_morph(game_no, name)
        except InitError as err:
            default_options = {field: values[0] for field, values in err.init_params.items()}
            morph = get_morph(game_no, name, **default_options)
            # TODO: Show form class
        vmorph = VirtualMorph(game_no=game_no, name=name)
        vmorph.morph = morph
        context['active_stats'] = {
            "current_cls": morph.current_cls,
            "current_lv": morph.current_lv,
            "numeric_stats": vmorph._generate_stats(),
        }
        return context

    def get_form_class(self):
        """
        """
        print("super().get_form_class())", super().get_form_class())
        print("get_form_class: self.request.path", self.request.path.split('/'))
        path = self.request.path.split('/')
        game_no = int(path[-3].replace("FE", ""))
        name = path[-2]
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        # TODO: Check to see if route-params are available at this stage.
        # Yep.
        return form_class 

class PreviewMorphView(TemplateView, FormView):
    """
    """
    template_name = "dracogate/_preview_morph.html"
    form_class = None

    def get_form_class(self):
        """
        """
        # TODO: Check to see if route-params are available at this stage.

    # TODO: Need to do research on htmx to progress.
    def get_context_data(self, game_no, name, **kwargs):
        """
        """
        try:
            morph = get_morph(game_no, name)
        except InitError as err:
            default_options = {field: values[0] for field, values in err.init_params.items()}
            morph = get_morph(game_no, name, **default_options)
            # TODO: Show form class
        vmorph = VirtualMorph(game_no=game_no, name=name)
        vmorph.morph = morph
        context['active_stats'] = {
            "current_cls": morph.current_cls,
            "current_lv": morph.current_lv,
            "numeric_stats": vmorph._generate_stats(),
        }
        return context
