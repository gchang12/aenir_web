"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError, UnitNotFoundError

from dracogate._logging import logger

def bundle_stats(morph):
    """
    """
    stats = []
    current_stats = morph.current_stats.as_dict()
    max_stats = morph.max_stats.as_dict()
    absmax_stats = morph.Stats.ABSOLUTE_MAXES()
    for indexno, stat in enumerate(morph.Stats.STAT_LIST()):
        stats.append((stat, current_stats[stat] / 100, max_stats[stat] / 100, absmax_stats[indexno]))
    return stats

def parse_request_into_args(request):
    """
    """
    game_no = int(request.query_params.get("game_no"))
    name = request.query_params.get("name")
    morph_options = (
        "father",
        "hard_mode",
        "number_of_declines",
        "route",
        "lyn_mode",
    )
    kwargs = {key: request.query_params.get(key) for key in morph_options if request.query_params.get(key) is not None}
    for kwarg, kwval in kwargs.items():
        if kwarg in ("hard_mode", "lyn_mode"):
            kwargs[kwarg] = {
                "true": True,
                "false": False,
            }[kwval]
        if kwarg == "number_of_declines":
            kwargs[kwarg] = int(kwval)
    return (game_no, name, kwargs)

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """
    morphs = {}

    def create(self, request):
        """
        """
        if len(morphs) == 5:
            raise Exception
        elif len(morphs) > 5:
            raise Exception
        morph_id = request.query_params.get("morph_id")
        if morph_id in morphs:
            raise Exception
        game_no, name, kwargs = parse_request_into_args(request)
        morph = get_morph(game_no, name, **kwargs)
        morph._set_max_level()
        # name, current, max, absMax
        stats = bundle_stats(morph)
        data = {
            "unitClass": morph.current_cls,
            "level": (morph.current_lv, morph.max_level),
            "stats": stats,
        }
        return Response({"id": morph_id, "morph": data})

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        game_no, name, kwargs = parse_request_into_args(request)
        logger.debug("game_no: %d, name: '%s', kwargs: %r", game_no, name, kwargs)
        try:
            morph = get_morph(game_no, name, **kwargs)
            morph._set_max_level()
            # name, current, max, absMax
            stats = bundle_stats(morph)
            data = {
                "unitClass": morph.current_cls,
                "level": (morph.current_lv, morph.max_level),
                "stats": stats,
            }
        except InitError as e:
            data = {"missingParams": e.init_params}
        except NotImplementedError:
            data = {"error": "INVALID_GAME"}
        except UnitNotFoundError:
            data = {"error": "UNIT_DNE"}
        return Response(data)

