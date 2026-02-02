#
"""
"""

from rest_framework.response import Response
from rest_framework import viewsets

from aenir import get_morph
from aenir._exceptions import InitError

class MorphViewSet(viewsets.ViewSet):
    """
    """
    queryset = None

    def list(self, request):
        """
        """
        more_info_needed: bool = False
        game_no = int(request.query_params.get("game_no"))
        name = request.query_params.get("name")
        kwargs = request.query_params.get("kwargs") or {}
        morph = get_morph(game_no, name, **kwargs)
        print(morph)
        data = morph.current_stats
        return Response([more_info_needed, data])

    def create(self, request):
        """
        """
        more_info_needed: bool = False
        game_no = request.data.get("game_no")
        name = request.data.get("name")
        kwargs = request.data.get("kwargs")
        return Response([more_info_needed, data])
