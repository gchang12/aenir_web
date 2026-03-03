"""
Interface to create and play with Morph objects.
"""

import json

from django.shortcuts import (
    get_object_or_404,
)

from rest_framework.decorators import action
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
        return Response(
            {
                "pk": pk,
            }
        )

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
        return Response(
            {
                "morphId": vmorph.morph_id,
                "initArgs": {
                    "gameNo": vmorph.game_no,
                    "unitName": vmorph.name,
                    "options": vmorph.options,
                },
                "morph": data,
                "history": vmorph.history,
            }
        )

    def simulate_operation(self, request, pk, method_name):
        """
        """
        vmorph = get_object_or_404(VirtualMorph, id=pk)
        morph = vmorph.init()
        morph._set_max_level()
        logger.debug("Attempting to validate 'method_name': '%s'.", method_name)
        method_serializer = MorphMethodArgs(data={"method_name": method_name})
        method_serializer.is_valid(raise_exception=True)
        (method, serializer) = {
            "level_up": (vmorph.level_up, LevelUpArgs),
            "promote": (vmorph.promote, PromoteArgs),
            "use_stat_booster": (vmorph.use_stat_booster, UseStatBoosterArgs),
            "equip_scroll": (vmorph.equip_scroll, ScrollEquipmentArgs),
            "unequip_scroll": (vmorph.unequip_scroll, ScrollEquipmentArgs),
            "use_afas_drops": (vmorph.use_afas_drops, NullDictSerializer),
            "use_metiss_tome": (vmorph.use_metiss_tome, NullDictSerializer),
            "equip_band": (vmorph.equip_band, BandEquipmentArgs),
            "unequip_band": (vmorph.unequip_band, BandEquipmentArgs),
            "equip_knight_ward": (vmorph.equip_knight_ward, NullDictSerializer),
            "unequip_knight_ward": (vmorph.unequip_knight_ward, NullDictSerializer),
        }[method_name]
        method_args_serializer = serializer(data=request.query_params)
        logger.debug("Attempting to validate argument(s) of '%s'.", method_name)
        method_args_serializer.is_valid(raise_exception=True)
        valid_method_args = method_args_serializer.validated_data
        logger.debug("Attempting to call `%s(**%r)`.", method_name, valid_method_args)
        try:
            (is_success, param_bounds) = method(**valid_method_args)
            logger.debug("vmorph.morph is morph: %r. morph.current_stats: %r", vmorph.morph is morph, morph.current_stats.as_dict())
        except NotImplementedError:
            # e.g., Morph4.use_afas_drops
            logger.debug("`%s` has not been implemented for `%s`.", method_name, vmorph.morph.__class__.__name__)
            raise exceptions.ParseError(
                code="METHOD_NOT_DEFINED_ON_MORPH",
                detail="The '%s' method is not defined on %s." % (method_name, vmorph.morph.__class__.__name__),
            )
        except Exception as err: # NOTE: Wasn't this caught back at the model layer..,?
            # e.g., Morph5.level_up(99)
            logger.critical("Calling `%s.%s(**%r)` has resulted in an unforeseen error: %r.", vmorph.morph.__class__.__name__, method_name, valid_method_args, err)
            raise exceptions.ParseError(
                code="METHOD_INVOCATION_FAILED",
                detail="%r" % err,
            )
        serializer = MorphSerializer(morph)
        statdicts = serializer.get_current_stats()
        data = serializer.get_morph(*statdicts)
        if request.method == "PATCH":
            if is_success is True:
                logger.debug("PATCH method was successful. Updating Morph object.")
                vmorph.save()
                return Response(
                    {
                        "morph": data,
                    }
                )
            elif is_success is False:
                logger.debug("PATCH method was unsuccessful. Not updating Morph object.")
                raise exceptions.ParseError(
                    code="UNABLE_TO_UPDATE",
                    detail="The program was unable to update your Morph.",
                )
        elif request.method == "GET":
            if is_success is True:
                #if method_name == "promote": raise Exception
                logger.debug("GET method was successful. Returning preview and parameter bounds.")
                return Response(
                    {
                        "paramBounds": param_bounds,
                        "morph": data,
                    }
                )
            elif is_success is False:
                #raise Exception
                logger.debug("GET method was unsuccessful. Returning parameter bounds.")
                return Response(
                    {
                        "paramBounds": param_bounds,
                        #"morph": data,
                    }
                )

    @action(detail=True, methods=["patch", "get"])
    def level_up(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "level_up"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def promote(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "promote"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def use_stat_booster(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "use_stat_booster"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def equip_scroll(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "equip_scroll"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def unequip_scroll(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "unequip_scroll"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def use_afas_drops(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "use_afas_drops"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def use_metiss_tome(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "use_metiss_tome"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def equip_band(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "equip_band"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def unequip_band(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "unequip_band"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def equip_knight_ward(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "equip_knight_ward"
        return self.simulate_operation(request, pk, method_name)

    @action(detail=True, methods=["patch", "get"])
    def unequip_knight_ward(self, request, pk):
        """
        Simulates operations on a morph without modifying it.
        """
        method_name = "unequip_knight_ward"
        return self.simulate_operation(request, pk, method_name)

