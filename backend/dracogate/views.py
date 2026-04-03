"""
"""

from django.shortcuts import render
from django.views.generic.base import TemplateView

from aenir.games import FireEmblemGame
from aenir import morph

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
        units = morph_cls.CHARACTER_LIST()
        context['game_no'] = game_no
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
        context['name'] = name
        return context
