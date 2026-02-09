"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError

from dracogate._logging import logger

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """
    morphs = {}

    def create(self, request):
        """
        Creates Morph object for user and initializes `morph` attribute to mirror user-actions.
        """
        if len(self.morphs) == 5:
            raise Exception
        id = request.data.get('id')
        if id in self.morphs:
            raise Exception
        game_no = int(request.data.get("game_no"))
        name = request.data.get("name")
        kwargs = json.loads(request.data.get("kwargs") or {})
        morph = get_morph(game_no, name, **kwargs)
        self.morphs[id] = morph
        return Response(data)

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        game_no = int(request.query_params.get("game_no"))
        name = request.query_params.get("name")
        kwarg_keys = (
            "father",
            "hard_mode",
            "number_of_declines",
            "route",
            "lyn_mode",
        )
        kwargs = {key: request.query_params.get(key) for key in kwarg_keys if request.query_params.get(key) is not None)}
        logger.debug("game_no: %d, name: '%s', kwargs: %r", game_no, name, kwargs)
        try:
            morph = get_morph(game_no, name, **kwargs)
            morph._set_max_level()
            data = {
                "currentCls": morph.current_cls,
                "currentLv": morph.current_lv,
                "currentStats": morph.current_stats.as_list(),
                "maxStats": morph.max_stats.as_list(),
                "maxLv": morph.max_level,
            }
        except InitError as e:
            data = {"missingParams": e.init_params}
        return Response((is_success, data))

