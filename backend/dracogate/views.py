from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response

from aenir import get_morph
from aenir.morph import (
    Morph4,
    Morph5,
    Morph6,
    Morph7,
    Morph8,
    Morph9,
)
from aenir._exceptions import InitError

from ._logging import logger

class InitializationViewset(viewsets.ViewSet):
    """
    """

    def list(self, request):
        """
        """
        def convert_js_boolean_to_python_boolean(value):
            try:
                return {
                    'true': True,
                    'false': False,
                }[value]
            except KeyError:
                return value
        data = {}
        for key, value in request.query_params.items():
            data[key] = convert_js_boolean_to_python_boolean(value)
        data['game_no'] = int(data.pop("game"))
        name = data.get("name")
        game = data.get('game_no')
        logger.debug("Getting character: %s from FE%d", name, game)
        try:
            morph = get_morph(**data)
            logger.debug("Got Morph%d instance of %s", game, name)
            return Response([
                True, {
                    "current_stats": morph.current_stats.as_list(),
                    "current_maxes": morph.max_stats.as_list(),
                    "current_cls": morph.current_cls,
                    "current_lv": morph.current_lv,
                }
            ])
        except InitError as err:
            logger.debug("Failed to fetch Morph%d!%s. Need extra data: %s, %s", game, name, err.init_params, err.init_params2)
            # implicit: bind first item of err-initparams to `missing_params`
            for missing_params in err.init_params.items():
                break
            # implicit: bind first item of err-initparams2 to `missing_params2` if applicable
            if err.init_params2 is None:
                missing_params2 = None
            else:
                for missing_params2 in err.init_params2.items():
                    break
            return Response([
                False, {
                    "missing_params": missing_params,
                    "missing_params2": missing_params2,
                }
            ])

    def create(self, request):
        """
        """
        # TODO: Use this for, like, saving the morph.
        # save to session or whatever
        print(request.data)
        return Response()

