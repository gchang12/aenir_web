"""
Views for interacting with Morph objects.
"""

from django.shortcuts import (
    render,
    redirect,
)
from django.views.generic.base import TemplateView
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import FormView
from django.urls import reverse
from django import forms
from django.http import Http404

import aenir.morph
import aenir.games
from aenir import get_morph
from aenir._exceptions import (
    InitError,
    UnitNotFoundError,
)

from .models import VirtualMorph
from .forms import InitFormBuilder
from ._logging import logger

class GameSelectView(TemplateView):
    """
    Displays list of hyperlinks for each game encompassed by aenir.
    """
    template_name = "dracogate/game_select.html"

    def get_context_data(self, **kwargs):
        """
        Inserts 'games' list into template context.
        """
        context = super().get_context_data(**kwargs)
        games = {game.value: game.formal_name for game in aenir.games.FireEmblemGame}
        context['games'] = games
        return context

class UnitSelectView(GameSelectView):
    """
    Displays list of hyperlinks for each unit for a given game.
    """
    template_name = "dracogate/unit_select.html"

    def get_context_data(self, game_no, **kwargs):
        """
        Inserts 'units' list and namespaced 'game_no' parameters into template context.
        """
        context = super().get_context_data(**kwargs)
        try:
            morph_cls = getattr(aenir.morph, "Morph%d" % game_no)
        except AttributeError:
            raise Http404("Sorry. Morph%d has not been implemented yet!" % game_no)
        units = morph_cls.CHARACTERS
        context['route_params'] = {}
        context['route_params']['game_no'] = game_no
        context['units'] = units
        return context

class UnitConfirmView(UnitSelectView, FormView):
    """
    Web interface for initializing a Morph instance.
    """
    template_name = "dracogate/unit_confirm.html"

    def get_context_data(self, game_no, name, **kwargs):
        """
        Adds the 'name' value to the namespace 'route_params' in the template context.
        """
        context = super().get_context_data(game_no, **kwargs)
        context['route_params']['name'] = name
        return context

    def get_form_class(self):
        """
        Returns a form class specific to the unit.
        """
        path = self.request.path.split('/')
        game_no = int(path[-3].replace("FE", ""))
        name = path[-2]
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        except UnitNotFoundError:
            raise Http404("'%s' is not an FE%d character." % (name, game_no))
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        return form_class 

    def form_valid(self, form):
        """
        Creates a VirtualMorph in the database.
        """
        # prepare data to be saved
        cleaned_data = form.cleaned_data
        game_no = cleaned_data.pop('game_no')
        name = cleaned_data.pop('name')
        options = cleaned_data
        logger.debug("Generating progress data for Morph%d('%s', **%r).", game_no, name, options)
        morph = get_morph(game_no, name, **options)
        progress = {
            "current_lv": morph.current_lv,
            "current_cls": morph.current_cls,
        }
        morph_id = VirtualMorph._generate_morph_id(game_no, name)
        owner = None
        vmorph = VirtualMorph.objects.create(
            owner=owner,
            morph_id=morph_id,
            game_no=game_no,
            name=name,
            options=options,
            progress=progress,
        )
        # generate success_url
        logger.debug("vmorph.id: %r, %r", vmorph.id, type(vmorph.id))
        success_url = reverse("dracogate:modify_morph", args=[vmorph.id])
        logger.debug("return: %r", success_url)
        return redirect(success_url)

class UnitConfirmPreviewView(TemplateView):
    """
    Shows initial stats of Morph instance given game_no, name, and options.
    """
    template_name = "dracogate/unit_confirm_preview.html"

    def get_context_data(self, game_no, name, **kwargs):
        """
        Generates variables for showing unit stats.
        """
        try:
            logger.debug("Attempting initialization of Morph%d('%s')", game_no, name)
            morph = get_morph(game_no, name)
        except InitError as err:
            logger.debug("Initialization failed. Updating Morph initialization parameters with GET parameters.")
            default_options = {field: values[0] for field, values in err.init_params.items()}
            specified_options = self.request.GET
            for param in default_options.keys():
                new_param_value = specified_options.get(param)
                if param in ("hard_mode", "lyn_mode"):
                    new_param_value = new_param_value == "on"
                elif param == "number_of_declines":
                    new_param_value = int(new_param_value or 0)
                if new_param_value is not None:
                    default_options[param] = new_param_value
            logger.debug("Reinitializing Morph with parameters: (game_no=%d, name='%s', **%r)", game_no, name, default_options)
            morph = get_morph(game_no, name, **default_options)
        vmorph = VirtualMorph(game_no=game_no, name=name)
        vmorph.morph = morph
        context = super().get_context_data(**kwargs)
        logger.debug("Setting template context variables.")
        context['route_params'] = {
            "game_no": game_no,
            "name": name,
        }
        context['active_stats'] = {
            "current_cls": morph.current_cls,
            "current_lv": morph.current_lv,
            "numeric_stats": vmorph._generate_stats(),
        }
        return context

class ListMorphsView(ListView):
    """
    Lists hyperlinks to VirtualMorph objects that can be accessed.
    """
    paginate_by = 50
    template_name = "dracogate/list_morphs.html"
    queryset = None
    model = VirtualMorph

    def get_context_data(self, **kwargs):
        """
        Default implementation.
        """
        context = super().get_context_data(**kwargs)
        logger.debug("context: %r", context)
        return context

    def get_queryset(self, **kwargs):
        """
        Sorts queryset by 'modification_date'.
        """
        queryset = super().get_queryset(**kwargs)
        return queryset.order_by("-modification_date")

# TODO: Test! Clean up!
# Clearly, this needs more planning.
# TODO: Insert URL list.
# TODO: Modify morph-preview view
# TODO: Make sure to disable the submit-button if the selection is invalid.

class ModifyMorphView(DetailView):
    """
    """
    template_name = "dracogate/modify_morph.html"
    model = VirtualMorph
    method_dict = {
        "level_up": "Level Up",
        "promote": "Promote",
        "use_stat_booster": "Use Stat Booster",
        "set_scrolls": "Equip Scrolls",
        "use_afas_drops": "Use Afa's Drops",
        "use_metiss_tome": "Use Metis's Tome",
        "set_bands": "Equip Bands",
        #"transform": "Transform",
        #"revert": "Revert",
        "shapeshift": "Transform",
    }

    def get_context_data(self, **kwargs):
        """
        """
        # 4: level_up, promote
        # 5: level_up, promote, use_stat_booster, set_scrolls
        # 6: level_up, promote, use_stat_booster
        # 7: level_up, promote, use_stat_booster, use_afas_drops
        # 8: level_up, promote, use_stat_booster, use_metiss_tome
        # 9: level_up, promote, use_stat_booster, set_bands, shapeshift
        context = super().get_context_data(**kwargs)
        return context

class ModifyMorphPreviewView(DetailView):
    """
    """
    template_name = "dracogate/modify_morph_preview.html"
    model = VirtualMorph

    def get_context_data(self, **kwargs):
        """
        """
        pk = self.object.pk
        context = super().get_context_data(**kwargs)
        vmorph = VirtualMorph.objects.get(pk=pk)
        morph = vmorph.init()
        context['route_params'] = {
            "game_no": vmorph.game_no,
            "name": vmorph.name,
        }
        context['active_stats'] = {
            "current_cls": morph.current_cls,
            "current_lv": morph.current_lv,
            "numeric_stats": vmorph._generate_stats(),
        }
        return context

