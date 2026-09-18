"""
"""

from django.views.generic import base, edit

from aenir.games import FireEmblemGame

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

# TODO: Figure out how to implement these

class UnitConfirmView(edit.CreateView):
    """
    """

class UnitConfirmForm(edit.FormView):
    """
    """
