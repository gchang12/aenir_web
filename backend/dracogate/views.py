"""
"""

from django.shortcuts import render
from django.views.generic.base import TemplateView

from aenir.games import FireEmblemGame

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
