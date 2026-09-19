"""
"""

from django.views.generic import base, edit

from aenir.games import FireEmblemGame
from aenir.morph import get_morph_class

from . import models

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

class UnitConfirmView(edit.CreateView):
    """
    """
    template_name = "dracogate/unit_confirm.html"
    model = models.VirtualMorph
    fields = []

    def get_context_data(self):
        """
        """
        #print(self, dir(self), self.args, self.kwargs, kwds)
        context = super().get_context_data(**self.kwargs)
        context.update(self.kwargs)
        return context

class UnitConfirmForecast(base.TemplateView):
    """
    """
