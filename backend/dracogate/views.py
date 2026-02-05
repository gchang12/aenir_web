"""
Interface to create and play with Morph objects.
"""

import json

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """
    morph = None

    def create(self, request):
        """
        Creates Morph object for user and initializes `morph` attribute to mirror user-actions.
        """
        game_no = int(request.data.get("game_no"))
        name = request.data.get("name")
        kwargs = json.loads(request.data.get("kwargs") or {})
        morph = get_morph(game_no, name, **kwargs)
        self.morph = morph
        return Response(data)

    def list(self, request):
        """
        Creates temporary Morph for the user to preview, returning missing parameters as necessary.
        """
        game_no = int(request.query_params.get("game_no"))
        name = request.query_params.get("name")
        #print(request.query_params.get("kwargs"))
        kwargs = json.loads(request.query_params.get("kwargs") or "{}")
        #print(game_no, name, kwargs)
        try:
            morph = get_morph(game_no, name, **kwargs)
            data = {
                "currentCls": morph.current_cls,
                "currentLv": morph.current_lv,
                "currentStats": morph.current_stats.as_list(),
                "currentMaxes": morph.max_stats.as_list(),
            }
            is_success = True
        except InitError as e:
            data = {"missingParams": e.init_params}
            is_success = False
        #print(data)
        return Response((is_success, data))

