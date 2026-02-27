"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError, UnitNotFoundError
from aenir_web._logging import logger

from dracogate.models import VirtualMorph
from dracogate.serializers import (
    #InitArgs,
    MorphSerializer,
)

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        #init_args_serializer = InitArgs(data=request.query_params)
        #init_args_serializer.is_valid(raise_exception=True)
        #options = init_args_serializer.validated_data
        #logger.debug("options: %r", options)
        #game_no = options.pop("game_no")
        #name = options.pop("name")
        game_no, name, options = MorphSerializer.parse_init_args(request.query_params)
        try:
            morph = get_morph(game_no, name, **options)
            morph._set_max_level()
            # name, current, max, absMax
            serializer = MorphSerializer(morph)
            statdicts = serializer.get_current_stats()
            data = serializer.get_morph(*statdicts)
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
        game_no, name, options = MorphSerializer.parse_init_args(request.data)
        morph = get_morph(game_no, name, **options)
        serializer = MorphSerializer(morph)
        statdicts = serializer.get_current_stats()
        data = serializer.get_morph(*statdicts)
        pk = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options).id
        return Response({
            "pk": pk,
            # NOTE: Include only the data to be shown for the brief description.
            "morphId": morph_id,
            "initArgs": {
                "gameNo": game_no,
                "unitName": name,
            },
            "level": data["level"],
            "unitClass": data['unitClass'],
        })

    def retrieve(self, request, pk):
        """
        """
        vmorph = VirtualMorph.objects.get(id=pk)
        morph = vmorph.init()
        serializer = MorphSerializer(morph)
        statdicts = serializer.get_current_stats()
        data = serializer.get_morph(*statdicts)
        return Response({
            "morphId": vmorph.morph_id,
            "initArgs": {
                "gameNo": vmorph.game_no,
                "unitName": vmorph.name,
                "options": vmorph.options,
            },
            "morph": data,
            "history": vmorph.history,
        })

    def partial_update(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        (is_success, param_bounds) = self.simulate_operation(request.data)
        morph = vmorph.init()
        serializer = MorphSerializer(morph)
        data = serializer.get_morph()
        return Response({
            #"morphId": vmorph.morph_id,
            #"initArgs": {
                #"gameNo": vmorph.game_no,
                #"unitName": vmorph.name,
                #"options": vmorph.options,
                #},
            #"morph": data,
            "paramBounds": param_bounds,
        })

    def update(self, request, pk):
        """
        Performs operations on a morph and modifies it.
        """
        (is_success, param_bounds) = self.simulate_operation(request.data)
        morph = vmorph.init()
        serializer = MorphSerializer(morph)
        data = serializer.get_morph()
        vmorph.save()
        return Response({
            #"morphId": vmorph.morph_id,
            #"initArgs": {
            #"gameNo": vmorph.game_no,
            #"unitName": vmorph.name,
            #"options": vmorph.options,
            #},
            "morph": data,
            #"paramBounds": param_bounds,
        })

    def destroy(self, request, pk):
        """
        For deleting morph objects from the viewset.
        """
        status = {"success": None}
        try:
            status['success'] = True
        except KeyError as err:
            status['success'] = False
        logger.debug("Morph with id=%r has been deleted: %r", pk, status['success'])
        return Response(status)

    @staticmethod
    def simulate_operation(dictlike):
        """
        """
        morph_id = dictlike.get("morph_id")
        method = dictlike.get("method")
        kwargs = dictlike.get("kwargs")
        pk = int(dictlike.get("pk"))
        vmorph = VirtualMorph.objects.get(id=pk)
        vmorph.init()
        (is_success, param_bounds) = {
            "level_up": vmorph.level_up,
            "promote": vmorph.promote,
            "use_stat_booster": vmorph.use_stat_booster,
            "use_afas_drops": vmorph.use_afas_drops,
            "use_metiss_tome": vmorph.use_metiss_tome,
            "equip_band": vmorph.equip_band,
            "unequip_band": vmorph.unequip_band,
            "equip_scroll": vmorph.equip_scroll,
            "unequip_scroll": vmorph.unequip_scroll,
        }[method](**kwargs)
        return param_bounds

