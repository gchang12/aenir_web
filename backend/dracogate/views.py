"""
"""

from django.views.generic.edit import (
    FormView,
)
from django.views.generic.base import (
    TemplateView,
)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from aenir.games import FireEmblemGame
from aenir import (
    InitError,
    PromotionError,
    get_morph,
    get_morph_class,
)

from dracogate.models import (
    VirtualMorph,
    StatsBundler,
)
from dracogate.forms import (
    InitFormBuilder,
    ActionFormBuilder,
)

def get_temp_morph(game_no, unit, init_options):
    """
    """
    # parse morph-init options
    def parse_init_option(init_option):
        """
        """
        key, value = init_option
        if key in ("lyn_mode", "hard_mode"):
            value = {
                "True": True,
                "False": False,
            }[value]
        elif key == "number_of_declines":
            value = int(value)
        return key, value
    option_fields = InitFormBuilder.OPTION_FIELDS()
    init_options = dict(
        map(
            parse_init_option,
            filter(
                lambda key_value: key_value[0] in option_fields,
                init_options.items(),
            )
        )
    )
    # try create morph and get new init_params
    try:
        temp_morph = get_morph(game_no, unit, **init_options)
        init_params = {}
    except InitError as e:
        init_params = e.init_params
        init_options.update({key: value[0] for key, value in init_params.items()})
        temp_morph = get_morph(game_no, unit, **init_options)
    return (init_params, temp_morph)

class GameSelectView(TemplateView):
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

class UnitSelectView(TemplateView):
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

class UnitConfirmView(FormView):
    """
    """
    template_name = "dracogate/unit_confirm.html"
    success_url = reverse_lazy("dracogate:morph_list")

    def get_context_data(self):
        """
        """
        #print("get_context_data", self.kwargs)
        context = super().get_context_data(**self.kwargs)
        context.update(self.kwargs)
        return context

    def get_form_class(self):
        """
        """
        #self.init_params = {}
        #form = super().get_form_class()
        #print(self.init_params)
        form_class = InitFormBuilder.build_form_class(self.init_params)
        #print(form_class.declared_fields)
        #print("get_form_class", form_class.declared_fields)
        return form_class

    def get(self, request, game_no, unit):
        """
        """
        (init_params, _) = get_temp_morph(game_no, unit, {})
        self.init_params = init_params
        self.route_params = {
            "game_no": game_no,
            "unit": unit,
        }
        return super().get(request, game_no, unit)

    def post(self, request, game_no, unit):
        """
        """
        (init_params, _) = get_temp_morph(game_no, unit, {})
        self.init_params = init_params
        self.route_params = {
            "game_no": game_no,
            "unit": unit,
        }
        #print("post", self.init_params)
        return super().post(request, game_no, unit)

    def form_valid(self, form):
        """
        """
        #print("form_valid", form.is_valid())
        #print("form_valid", form.declared_fields)
        #print("form_valid", form.cleaned_data)
        #print("form_valid", self.route_params)
        VirtualMorph.objects.create(
            owner=(self.request.user if self.request.user.is_authenticated else None),
            game_no=self.route_params.pop("game_no"),
            unit=self.route_params.pop("unit"),
            init_options=form.cleaned_data,
        )
        return super().form_valid(form)

class UnitConfirmForecast(TemplateView):
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
        context['stats'] = StatsBundler.init_forecast(morph)
        context['unit_level'] = morph.current_lv
        context['unit_class'] = morph.current_cls
        #print(context)
        return context

class MorphListView(ListView):
    """
    """
    template_name = "dracogate/morph_list.html"
    model = VirtualMorph

    def get_context_data(self, **kwargs):
        """
        """
        context = super().get_context_data(**kwargs)
        #print(context)
        return context

    def get_queryset(self):
        """
        """
        #print(dir(self))
        owner = (None if not self.request.user.is_authenticated else self.request.user)
        queryset = self.model.objects.filter(owner=owner).order_by("-creation_date")
        return queryset

class MorphDetailView(DetailView):
    """
    """
    template_name = "dracogate/morph_detail.html"
    model = VirtualMorph
    init_option_dict = {
        "father": "Father",
        "hard_mode": "Hard Mode",
        "number_of_declines": "Declines",
        "chapter": "Chapter",
        "lyn_mode": "Lyn Mode",
    }
    action_name_dict = {
        "level_up": "Level Up",
        "promote": "Promote",
        "use_stat_booster": "Use Stat Booster",
        "use_afas_drops": "Use Afa's Drops",
        "use_metiss_tome": "Use Metis's Tome",
        "set_scrolls": "Equip Scrolls",
        "set_bands": "Equip Bands",
        "shapeshift": "Shapeshift", # transform/revert
        "set_demiband": "Toggle Demi Band",
    }
    actions_by_game = {
        4: (
            "level_up",
            "promote",
        ),
        5: (
            "level_up",
            "promote",
            "use_stat_booster",
            "set_scrolls",
        ),
        6: (
            "level_up",
            "promote",
            "use_stat_booster",
        ),
        7: (
            "level_up",
            "promote",
            "use_stat_booster",
            "use_afas_drops",
        ),
        8: (
            "level_up",
            "promote",
            "use_stat_booster",
            "use_metiss_tome",
        ),
        9: (
            "level_up",
            "promote",
            "use_stat_booster",
            "shapeshift",
            "set_bands",
            "set_demiband",
        ),
    }

    def get_context_data(self, object):
        """
        """
        context = super().get_context_data()
        morph = self.object.init()
        context['init_options'] = {self.init_option_dict[key]: value for key, value in self.object.init_options.items()}
        context['stats'] = StatsBundler.init_forecast(morph)
        app_name = "dracogate"
        context['actions'] = map(
            lambda action: (app_name + ":" + action, self.action_name_dict[action]),
            self.actions_by_game[self.object.game_no],
        )
        context['history'] = self.object.history
        context["unit_class"] = morph.current_cls
        context["unit_lv"] = morph.current_lv
        return context

    def get_object(self):
        """
        """
        id = self.request.path.split('/')[-2]
        obj = self.model.objects.get(id=id)
        return obj

class ActionForecastView(DetailView):
    """
    """
    template_name = "dracogate/action_forecast.html"
    model = VirtualMorph

    def get_object(self):
        """
        """
        id = self.request.path.split('/')[-3]
        obj = self.model.objects.get(id=id)
        obj.init()
        return obj

    def get_context_data(self, **kwds):
        """
        """
        action = self.request.GET.get('action')
        stat_type = self.request.GET['stat_type']
        context = super().get_context_data(**kwds)
        morph = self.object.morph.copy()
        context['before'] = {
            "unit_class": morph.current_cls,
            "unit_lv": morph.current_lv,
        }
        context['before']['numeric_stats'] = {
            "bases": StatsBundler.action_forecast_bases,
            "growths": StatsBundler.action_forecast_growths,
        }[stat_type](morph, None)
        {
            None: lambda: None,
            "level_up": self.level_up,
            "promote": self.promote,
            "use_stat_booster": self.use_stat_booster,
            "use_afas_drops": self.use_afas_drops,
        }[action]()
        delta_dict = {
            "bases": (self.object.morph.current_stats > morph.current_stats).as_dict,
            "growths": (self.object.morph.growth_rates > morph.growth_rates).as_dict,
        }[stat_type]()
        context['after'] = {
            "unit_class": self.object.morph.current_cls,
            "unit_lv": self.object.morph.current_lv,
        }
        context['after']['numeric_stats'] = {
            "bases": StatsBundler.action_forecast_bases(self.object.morph, delta_dict),
            "growths": StatsBundler.action_forecast_growths(self.object.morph, delta_dict),
        }[stat_type]
        return context

    def level_up(self):
        """
        """
        num_levels = int(self.request.GET["target_lv"]) - self.object.morph.current_lv
        self.object.level_up(num_levels)

    def promote(self):
        """
        """
        promo_cls = self.request.GET["promo_cls"]
        self.object.promote(promo_cls)

    def use_stat_booster(self):
        """
        """
        item_name = self.request.GET["item_name"]
        self.object.use_stat_booster(item_name)

    def use_afas_drops(self):
        """
        """
        to_consume = self.request.GET.get("to_consume")
        self.object.use_afas_drops(to_consume == "True")

class MorphActionView(FormView, DetailView):
    """
    """
    template_name = "dracogate/morph_action.html"
    model = VirtualMorph
    action = {
        "title": None,
        "name": None,
        "stat_type": None,
    }

    def get_object(self):
        """
        """
        id = self.request.path.split('/')[-3]
        obj = self.model.objects.get(id=id)
        obj.init()
        return obj

    def get_context_data(self, **kwds):
        """
        """
        context = super().get_context_data(**kwds)
        context['action'] = self.action
        return context

class LevelUpView(MorphActionView):
    """
    """
    action = {
        "title": "Level Up",
        "name": "level_up",
        "stat_type": "bases",
    }

    def get_context_data(self, **kwds):
        """
        """
        context = super().get_context_data(**kwds)
        morph = self.object.morph
        is_success = not (morph.max_level == morph.current_lv)
        context['is_success'] = is_success
        return context

    def get_form_class(self, **kwds):
        """
        """
        #print(dir(self), self.object, kwds, id)
        try:
            (_, param_bounds) = self.object.level_up(0)
        except AttributeError:
            self.object = self.get_object()
            (_, param_bounds) = self.object.level_up(0)
        if self.object.morph.current_lv == self.object.morph.max_level:
            param_bounds['min_lv'] = None
        form_class = ActionFormBuilder.level_up(param_bounds)
        return form_class

    def form_valid(self, form):
        """
        """
        num_levels = form.cleaned_data['target_lv'] - self.object.morph.current_lv
        #print(self.object.morph.current_stats.as_dict())
        self.object.level_up(num_levels)
        self.object.save()
        return redirect(reverse("dracogate:morph_detail", kwargs={"id": self.object.id}))


class PromoteView(MorphActionView):
    """
    """
    action = {
        "title": "Promote",
        "name": "promote",
        "stat_type": "bases",
    }

    def get_context_data(self, **kwds):
        """
        """
        #print('get_context_data')
        context = super().get_context_data(**kwds)
        morph = self.object.morph.copy()
        is_success: bool
        try:
            #print(morph.current_cls)
            morph.promote("")
            is_success = True
        except PromotionError as e:
            is_success = {
                e.Reason.NO_PROMOTIONS: False,
                e.Reason.LEVEL_TOO_LOW: True,
                e.Reason.INVALID_PROMOTION: True,
            }[e.reason]
            #print(e.reason)
        #print(is_success)
        context['is_success'] = is_success
        return context

    def get_form_class(self, **kwds):
        """
        """
        #print(dir(self), self.object, kwds, id)
        #print('get_form_class')
        try:
            (_, param_bounds) = self.object.promote("")
        except AttributeError:
            self.object = self.get_object()
            (_, param_bounds) = self.object.promote("")
        form_class = ActionFormBuilder.promote(param_bounds, self.object.morph)
        return form_class

    def form_valid(self, form):
        """
        """
        promo_cls = form.cleaned_data['promo_cls']
        #print(self.object.morph.current_stats.as_dict())
        #print(promo_cls)
        self.object.promote(promo_cls)
        self.object.save()
        return redirect(reverse("dracogate:morph_detail", kwargs={"id": self.object.id}))

# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
class UseStatBoosterView(MorphActionView):
    """
    """
    action = {
        "title": "Use Stat Booster",
        "name": "use_stat_booster",
        "stat_type": "bases",
    }

    def get_context_data(self, **kwds):
        """
        """
        context = super().get_context_data(**kwds)
        is_success: bool = True
        context['is_success'] = is_success
        return context

    def get_form_class(self, **kwds):
        """
        """
        try:
            (_, param_bounds) = self.object.use_stat_booster("")
        except AttributeError:
            self.object = self.get_object()
            (_, param_bounds) = self.object.use_stat_booster("")
        form_class = ActionFormBuilder.use_stat_booster(param_bounds, self.object.morph)
        return form_class

    def form_valid(self, form):
        """
        """
        item_name = form.cleaned_data['item_name']
        self.object.use_stat_booster(item_name)
        self.object.save()
        return redirect(reverse("dracogate:morph_detail", kwargs={"id": self.object.id}))

# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
class UseAfasDropsView(MorphActionView):
    """
    """
    action = {
        "title": "Use Afa's Drops",
        "name": "use_afas_drops",
        "stat_type": "growths",
    }

    def get_context_data(self, **kwds):
        """
        """
        context = super().get_context_data(**kwds)
        is_success: bool = self.object.morph._miscellany["Afa's Drops"] is None
        #print(self.object.morph._miscellany)
        context['is_success'] = is_success
        return context

    def get_form_class(self, **kwds):
        """
        """
        try:
            (_, param_bounds) = self.object.use_afas_drops(False)
        except AttributeError:
            self.object = self.get_object()
            (_, param_bounds) = self.object.use_afas_drops(False)
        form_class = ActionFormBuilder.use_afas_drops(param_bounds, self.object.morph)
        return form_class

    def form_valid(self, form):
        """
        """
        #to_consume = form.cleaned_data['to_consume']
        self.object.use_afas_drops(True)
        self.object.save()
        return redirect(reverse("dracogate:morph_detail", kwargs={"id": self.object.id}))


