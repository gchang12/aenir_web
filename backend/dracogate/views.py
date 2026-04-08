"""
"""

from django.shortcuts import (
    render,
    redirect,
)
from django.views.generic.base import TemplateView
# TODO: Should this be a mix-in?
from django.views.generic.edit import FormView
from django.urls import reverse
from django import forms

import aenir.morph
import aenir.games
# TODO: Import all exceptions into 'aenir' for semantics' sake.
from aenir import get_morph
from aenir._exceptions import (
    InitError,
)

from .models import VirtualMorph
from .forms import InitFormBuilder
from ._logging import logger

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
        #print("super().get_form_class())", super().get_form_class())
        #print("get_form_class: self.request.path", self.request.path.split('/'))
        path = self.request.path.split('/')
        game_no = int(path[-3].replace("FE", ""))
        name = path[-2]
        try:
            get_morph(game_no, name)
            init_params = {}
        except InitError as e:
            init_params = e.init_params
        form_class = InitFormBuilder.build_form_class(game_no, name, init_params)
        return form_class 

    def form_valid(self, form):
        """
        """
        cleaned_data = form.cleaned_data
        # prepare data to be saved.
        game_no = cleaned_data.pop('game_no')
        name = cleaned_data.pop('name')
        options = cleaned_data
        if self.request.user.username == "":
            owner = None
        else:
            owner = self.request.user
        morph_id = VirtualMorph._generate_morph_id(game_no, name)
        # create morph
        vmorph = VirtualMorph.objects.create(
            owner=owner,
            morph_id=morph_id,
            game_no=game_no,
            name=name,
            options=options,
        )
        success_url = reverse("dracogate:modify_morph", args=[vmorph.id])
        logger.debug("return: %r", success_url)
        # redirect to `success_url`
        #return super().form_valid(form)
        return redirect(success_url)

class PreviewMorphView(TemplateView):
    """
    """
    template_name = "dracogate/_preview_morph.html"
    form_class = None

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

class ModifyMorphView(TemplateView):
    """
    """
    template_name = "dracogate/modify_morph.html"
