"""
Interface to create and play with Morph objects.
"""

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError

class MorphViewSet(viewsets.ViewSet):
    """
    Handles creation and editing of Morph objects.
    """

    def create(self, request):
        """
        Attempts to initialize Morph using `request.{game_no,name,kwargs}`.
        """
        game_no = int(request.data.get("game_no"))
        name = request.data.get("name")
        kwargs = request.data.get("kwargs") or {}
        try:
            morph = get_morph(game_no, name, **kwargs)
            data = {
                "currentCls": morph.current_cls,
                "currentLv": morph.current_lv,
                "currentStats": morph.current_stats,
                "currentMaxes": morph.max_stats,
            }
            success = True
        except InitError as e:
            data = e.init_params
            success = False
        return Response((success, data))
