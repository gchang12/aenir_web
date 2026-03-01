"""
Interface to create and play with Morph objects.
"""

import json

from django.shortcuts import (
    get_object_or_404,
)

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
        # NOTE: This results in many errors that cannot be verified before taking the leap, so to speak. Some errors include: Morph subclasses receiving unexpected arguments.
        game_no, name, options = MorphSerializer.parse_init_args(request.query_params)
        '''
        serializer = InitArgs(data=request.query_params)
        if not serializer.is_valid():
            raise Exception
        kwargs = serializer.validated_data
        '''
        try:
            morph = get_morph(game_no, name, **options)
            morph._set_max_level()
            serializer = MorphSerializer(morph)
            statdicts = serializer.get_current_stats()
            data = serializer.get_morph(*statdicts)
        except InitError as err:
            data = {"missingParams": err.init_params}
        except NotImplementedError as err:
            raise exceptions.NotFound(
                code="INVALID_GAME",
                detail="%r" % err,
            )
        except UnitNotFoundError as err:
            raise exceptions.NotFound(
                code="UNIT_DNE",
                detail="%r" % err,
            )
        return Response(data)

    def create(self, request):
        """
        Creates a Morph instance and stores it in the database.
        """
        morph_id_serializer = MorphIDSerializer(data={"morph_id": request.data.get("morph_id")})
        if not morph_id_serializer.is_valid():
            raise exceptions.ParseError(
                code="INVALID_MORPH_ID",
                detail="The value provided for 'morph_id' was too long.",
            )
        morph_id = morph_id_serializer.validated_data.pop("morph_id")
        game_no, name, options = MorphSerializer.parse_init_args(request.data)
        logger.debug("Nothing can be validated until the arguments are used to generate a Morph. Trying it now.")
        try:
            morph = get_morph(game_no, name, **options)
        except InitError as err:
            raise exceptions.NotFound(
                code="UNIT_DNE",
                detail="%r" % err,
            )
        except NotImplementedError as err:
            raise exceptions.NotFound(
                code="INVALID_GAME",
                detail="%r" % err,
            )
        except UnitNotFoundError as err:
            raise exceptions.NotFound(
                code="UNIT_DNE",
                detail="%r" % err,
            )
        pk = VirtualMorph.objects.create(morph_id=morph_id, game_no=game_no, name=name, options=options).id
        return Response({
            "pk": pk,
        })

    def destroy(self, request, pk):
        """
        For deleting morph objects from the viewset.
        """
        (delcount, detail) = VirtualMorph.objects.filter(id=pk).delete()
        if delcount == 0:
            raise exceptions.NotFound(
                code="VIRTUALMORPH_NOT_FOUND",
                detail="No VirtualMorph with id='%d' was found.",
            )
        return Response()

    def retrieve(self, request, pk):
        """
        """
        vmorph = get_object_or_404(VirtualMorph, id=pk)
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
        vmorph = VirtualMorph.objects.get(id=pk)
        morph = vmorph.init()
        (is_success, param_bounds) = self.simulate_operation(vmorph, request.data)
        serializer = MorphSerializer(morph)
        data = serializer.get_morph()
        return Response({
            "paramBounds": param_bounds,
        })

    def update(self, request, pk):
        """
        Performs operations on a morph and modifies it.
        """
        vmorph = VirtualMorph.objects.get(id=pk)
        morph = vmorph.init()
        (is_success, param_bounds) = self.simulate_operation(vmorph, request.data)
        serializer = MorphSerializer(morph)
        data = serializer.get_morph()
        vmorph.save()
        return Response({
            "morph": data,
        })

    @staticmethod
    def simulate_operation(vmorph, dictlike):
        """
        """
        raw_data = MorphMethodArgs(dictlike)
        if not raw_data.is_valid():
            raise exceptions.NotFound(
                code="BAD_MORPH_METHOD",
                detail="'%(method_name)s' is not a valid Morph method. %(args)r must be dict-like object." % raw_data.data,
            )
        data = raw_data.validated_data
        method_name = data.pop("method_name")
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
            raise exceptions.NotFound(
                code="BAD_MORPH_METHOD_ARGUMENTS",
                detail="Bad arguments were supplied for the '%s' method." % method_name,
            )
        method_args = method_arg_serializer.validated_data
        return method(**method_args)

