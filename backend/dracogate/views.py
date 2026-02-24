"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError, UnitNotFoundError

from aenir_web._logging import logger
from dracogate.models import Morph

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        game_no, name, kwargs = self.parse_init_args(request.query_params)
        try:
            morph = get_morph(game_no, name, **kwargs)
            morph._set_max_level()
            # name, current, max, absMax
            statdicts = self.serialize_current_stats(morph)
            data = self.serialize_morph(morph, *statdicts)
        except InitError as e:
            data = {"missingParams": e.init_params}
        except NotImplementedError:
            data = {"error": "INVALID_GAME"}
        except UnitNotFoundError:
            data = {"error": "UNIT_DNE"}
        return Response(data)

    def create(self, request):
        """
        Creates a Morph instance and stores it in the database.
        """
        morph_id = request.data.get("morph_id")
        game_no, name, kwargs = self.parse_init_args(request.data)
        morph = get_morph(game_no, name, **kwargs)
        morph._set_max_level()
        self.morphs[morph_id] = morph
        # name, current, max, absMax
        statdicts = self.serialize_current_stats(morph)
        data = self.serialize_morph(morph, *statdicts)
        id = Morph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=kwargs).id
        return Response({
            "pk": pk,
            "morphId": morph_id,
            "initArgs": {
                "gameNo": game_no,
                "unitName": name,
                "options": options,
            },
            "stats": data,
        })

    def retrieve(self, request, pk):
        """
        """

    def partial_update(self, request):
        """
        Simulates operations on a morph without modifying it.
        """
        morph_id = request.data.get("morph_id")
        if morph_id not in self.morphs:
            raise Exception
        morph = self.morphs[morph_id].copy()
        method = request.data.get("method")
        kwargs = request.data.get("kwargs")
        error = {
            "level_up": self.level_up,
            "promote": self.promote,
            "use_stat_booster": self.use_stat_booster,
            "use_afas_drops": self.use_afas_drops,
            "use_metiss_tome": self.use_metiss_tome,
            "equip_band": self.equip_band,
            "unequip_band": self.unequip_band,
            "equip_scroll": self.equip_scroll,
            "unequip_scroll": self.unequip_scroll,
        }[method](morph, **kwargs)
        # TODO: Refactor code s.t. stat formats are selected also.
        return self.serialize_morph(morph)

    def update(self, request):
        """
        Performs operations on a morph and modifies it.
        """
        morph_id = request.data.get("morph_id")
        if morph_id not in self.morphs:
            raise Exception
        morph = self.morphs[morph_id]
        method = request.data.get("method")
        kwargs = request.data.get("kwargs")
        is_success, value = {
            "level_up": self.level_up,
            "promote": self.promote,
            "use_stat_booster": self.use_stat_booster,
            "use_afas_drops": self.use_afas_drops,
            "use_metiss_tome": self.use_metiss_tome,
            "equip_band": self.equip_band,
            "unequip_band": self.unequip_band,
            "equip_scroll": self.equip_scroll,
            "unequip_scroll": self.unequip_scroll,
        }[method](morph, **kwargs)
        #statdicts = serializer(morph)
        # TODO: Refactor code s.t. stat formats are selected also.
        return self.serialize_morph(morph)

    def destroy(self, request, pk):
        """
        For deleting morph objects from the viewset.
        """
        status = {"success": None}
        try:
            self.morphs.pop(pk)
            status['success'] = True
        except KeyError as err:
            status['success'] = False
        logger.debug("Morph with id=%r has been deleted: %r", pk, status['success'])
        return Response(status)

    @staticmethod
    def parse_init_args(dictlike):
        """
        Parses default values from response and converts them for interpretation by program.
        """
        game_no = int(dictlike.get("game_no"))
        name = dictlike.get("name")
        morph_options = (
            "father",
            "hard_mode",
            "number_of_declines",
            "route",
            "lyn_mode",
        )
        kwargs = {key: dictlike.get(key) for key in morph_options if dictlike.get(key) is not None}
        for kwarg, kwval in kwargs.items():
            if kwarg in ("hard_mode", "lyn_mode"):
                kwargs[kwarg] = {
                    "true": True,
                    "false": False,
                }[kwval]
            if kwarg == "number_of_declines":
                kwargs[kwarg] = int(kwval)
        return (game_no, name, kwargs)

