"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import (
    viewsets,
    status,
    exceptions,
)

from aenir import get_morph
from aenir._exceptions import InitError, UnitNotFoundError
from aenir_web._logging import logger

from dracogate.models import VirtualMorph
from dracogate.serializers import (
    InitArgs,
    MorphMethodArgs,
    LevelUpArgs,
    PromoteArgs,
    UseStatBoosterArgs,
    ScrollEquipmentArgs,
    BandEquipmentArgs,
    MorphIDSerializer,
    # own
    MorphSerializer,
    NullDictSerializer,
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
        #options = request.query_params.pop("options")
        game_no, name, options = MorphSerializer.parse_init_args(request.query_params)
        # NOTE: This results in many errors, some of which include: Morph subclasses receiving unexpected arguments.
        '''
        serializer = InitArgs(data=request.query_params)
        if not serializer.is_valid():
            raise Exception
        kwargs = serializer.validated_data
        '''
        #kwargs = {"status": None}
        try:
            morph = get_morph(game_no, name, **options)
            #morph = get_morph(**kwargs)
            morph._set_max_level()
            # name, current, max, absMax
            serializer = MorphSerializer(morph)
            statdicts = serializer.get_current_stats()
            data = serializer.get_morph(*statdicts)
            #kwargs["status"] = status.HTTP_200_OK
        except InitError as err:
            data = {"missingParams": err.init_params}
            #kwargs["status"] = status.HTTP_200_OK
        # TODO: Learn more about the types of exceptions one can throw.
        except NotImplementedError as err:
            #data = {"error": "INVALID_GAME"}
            #kwargs["status"] = status.HTTP_404_NOT_FOUND
            raise exceptions.NotFound(
                code="INVALID_GAME",
                detail="%r" % err,
            )
        except UnitNotFoundError as err:
            #data = {"error": "UNIT_DNE"}
            #kwargs["status"] = status.HTTP_404_NOT_FOUND
            raise exceptions.NotFound(
                code="UNIT_DNE",
                detail="%r" % err,
            )
        return Response(data)

    def create(self, request):
        """
        Creates a Morph instance and stores it in the database.
        """
        morph_id_serializer = MorphIDSerializer(data={"morph_id": request.data.pop("morph_id")})
        if not morph_id_serializer.is_valid():
            raise Exception
        #options = request.
        game_no, name, options = MorphSerializer.parse_init_args(request.data)
        # NOTE: It's not going to be possible to validate anything until the data is used to try to create a Morph.
        try:
            morph = get_morph(game_no, name, **options)
        # TODO: Learn more about the types of exceptions one can throw.
        except InitError as e:
            raise Exception
        except NotImplementedError:
            raise Exception
        except UnitNotFoundError:
            raise Exception
        #serializer = MorphSerializer(morph)
        #statdicts = serializer.get_current_stats()
        #data = serializer.get_morph(*statdicts)
        pk = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options).id
        return Response({
            "pk": pk,
            # NOTE: Include only the data to be shown for the brief description.
            #"morphId": morph_id,
            #"initArgs": {
                #"gameNo": game_no,
                #"unitName": name,
                #},
            #"morph": {
                #"level": data["level"],
                #"unitClass": data['unitClass'],
                #},
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
        status = {"pk": None}
        try:
            status['pk'] = pk
        except KeyError as err:
            status['pk'] = None
        logger.debug("Morph with id=%r has been deleted: %r", pk, status['success'])
        return Response(status)

    @staticmethod
    def simulate_operation(vmorph, dictlike):
        """
        """
        #morph_id = dictlike.get("morph_id")
        #method = dictlike.get("method")
        #kwargs = dictlike.get("kwargs")
        #pk = int(dictlike.get("pk"))
        raw_data = MorphMethodArgs(dictlike)
        if not raw_data.is_valid():
            raise Exception
        data = raw_data.validated_data
        method_name = data.pop("method_name")
        vmorph = VirtualMorph.objects.get(id=pk)
        vmorph.init()
        (method, serializer) = {
            "level_up": (vmorph.level_up, LevelUpArgs),
            "promote": (vmorph.promote, PromoteArgs),
            "use_stat_booster": (vmorph.use_stat_booster, UseStatBoosterArgs),
            "use_afas_drops": (vmorph.use_afas_drops, NullDictSerializer),
            "use_metiss_tome": (vmorph.use_metiss_tome, NullDictSerializer),
            "equip_band": (vmorph.equip_band, BandEquipmentArgs),
            "unequip_band": (vmorph.unequip_band, BandEquipmentArgs),
            "equip_scroll": (vmorph.equip_scroll, ScrollEquipmentArgs),
            "unequip_scroll": (vmorph.unequip_scroll, ScrollEquipmentArgs),
        }[method_name]
        method_arg_serializer = serializer(data=data.pop("args"))
        if not method_arg_serializer.is_valid():
            raise Exception
        method_args = method_arg_serializer.validated_data
        return method(**method_args)

