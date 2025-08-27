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

    def create(self, request):
        """
        """
        data = request.data['data']
        data['game_no'] = int(data.pop("game"))
        name = data.get("name")
        game = data.get('game_no')
        logger.debug("Getting character: %s from FE%d", name, game)
        try:
            morph = get_morph(**data)
            logger.debug("Got Morph%d instance of %s", game, name)
            return Response([
                True, {
                    "stats": morph.current_stats.as_list(),
                    "maxes": morph.max_stats.as_list(),
                    "cls": morph.current_cls,
                    "lv": morph.current_lv,
                }
            ])
        except InitError as err:
            logger.debug("Failed to fetch Morph%d!%s. Need extra data: %s", game, name, err.init_params)
            return Response([
                False, {
                    "params": err.init_params,
                    "params2": err.init_params2,
                }
            ])

    def update(self, request):
        """
        """
        # TODO: Use this for, like, saving the morph.
