"""
"""

from django.views.generic import base, edit

from aenir.games import FireEmblemGame

class CreateMorphView(base.TemplateView):
    """
    """
    template_name = "dracogate/morph_init.html"

    def get_context_data(self, **kwds):
        """
        """
        print(kwds)
        context = super().get_context_data(**kwds)
        context['games'] = [
            {
                "title": fe_game.formal_name,
                "game_no": fe_game.value,
            } for fe_game in FireEmblemGame
        ]
        return context

class GameSelectView(base.TemplateView):
    """
    """

# TODO: Figure out how to implement these

class UnitSelectView(edit.CreateView):
    """
    """

class UnitSelectForm(edit.FormView):
    """
    """
