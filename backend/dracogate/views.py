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
from dracogate.serializers import MorphSerializer

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        game_no, name, kwargs = MorphSerializer.parse_init_args(request.query_params)
        try:
            morph = get_morph(game_no, name, **kwargs)
            morph._set_max_level()
            # name, current, max, absMax
            serializer_queue = MorphSerializer(morph)
            statdicts = serializer_queue.get_current_stats()
            data = serializer_queue.get_morph(*statdicts)
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
        game_no, name, kwargs = MorphSerializer.parse_init_args(request.data)
        morph = get_morph(game_no, name, **kwargs)
        morph._set_max_level()
        # name, current, max, absMax
        serializer_queue = MorphSerializer(morph)
        statdicts = serializer_queue.get_current_stats()
        data = serializer_queue.get_morph(*statdicts)
        id = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=kwargs).id
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
        (vmorph, serializer_queue) = self.simulate_operation(request.data)
        return serializer_queue.get_morph()

    def update(self, request, pk):
        """
        Performs operations on a morph and modifies it.
        """
        (vmorph, serializer_queue) = self.simulate_operation(request.data)
        vmorph.save()
        return serializer_queue.get_morph()

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
        vmorph = VirtualMorph.objects.get(pk=dictlike.get("pk"))
        vmorph.init()
        morph, param_bounds = {
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
        serializer_queue = MorphSerializer(morph)
        return (vmorph, serializer_queue)

