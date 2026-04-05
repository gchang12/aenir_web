"""
"""

from django.shortcuts import render
from django.views.generic.base import TemplateView

from aenir.games import FireEmblemGame
from aenir import morph
from aenir import get_morph
from aenir._exceptions import InitError

from .models import VirtualMorph

class GameSelectView(TemplateView):
    """
    """
    template_name = "dracogate/game_select.html"

    def get_context_data(self, **kwargs):
        """
        """
        context = super().get_context_data(**kwargs)
        games = {game.value: game.formal_name for game in FireEmblemGame}
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
        morph_cls = getattr(morph, "Morph%d" % game_no)
        units = morph_cls.get_true_character_list()
        context['GAME_NO'] = game_no
        context['units'] = units
        return context

class UnitConfirmView(UnitSelectView):
    """
    """
    template_name = "dracogate/unit_confirm.html"

    def get_context_data(self, game_no, name, **kwargs):
        """
        """
        context = super().get_context_data(game_no, **kwargs)
        context['NAME'] = name
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
