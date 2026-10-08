"""
"""

# TODO: Handle game-exclusive methods
# TODO: Forbid user from invoking methods that are invalid in a given Morph class.
# TODO: Make sure user can see and access only his own VirtualMorph objects.

class ForbidForbiddenMethodMixin:
    """
    """

    def dispatch(self, request, **kwds):
        """
        """
        owner = (None if self.request.user.is_authenticated is False else self.request.user)
        # forbid users who don't own objects from interacting with vmorph.
        if self.object.owner is not None and self.object.owner != owner:
            # redirect to create new morph page?
            # redirect to login page?
            raise Http403
        # forbid bad methods.
        if self.object.game_no not in self.valid_games:
            raise Http400
        return super().dispatch(request, **kwds)

class ForbidBadUserMixin:
    """
    """

    def dispatch(self, request, **kwds):
        """
        """
        owner = (None if self.request.user.is_authenticated is False else self.request.user)
        # forbid users who don't own objects from interacting with vmorph.
        if self.object.owner is not None and self.object.owner != owner:
            # redirect to login page?
            raise Http403
        return super().dispatch(request, **kwds)


class RedirectToMorphListMixin:
    """
    Tells user to select from list.
    """

    @staticmethod
    def redirect_to_morph_list(dispatch):
        """
        """
        def new_dispatch(self, request, **kwds):
            """
            """
            if request.user.is_authenticated is True and self.object.owner is not None:
                return redirect("dracogate:morph_list")
            return dispatch(self, request, **kwds)
        return new_dispatch

# TODO: Mixin for 'redirect-to-login' maybe?

class RedirectToLoginMixin:
    """
    """

    @staticmethod
    def redirect_to_login(dispatch):
        """
        """
        def new_dispatch(self, request, **kwds):
            """
            """
            if request.user.is_authenticated is True and self.object.owner is not None:
                return redirect("login")
            return dispatch(self, request, **kwds)
        return new_dispatch

class RedirectToMorphCreationMixin:
    """
    Tells user to get his own thing provided he's got his own account.
    """

    # TODO: This should be a decorator.
    def dispatch(self, request, **kwds):
        """
        """
        if request.user.is_authenticated is True and self.object.owner != request.user:
            kwargs = {
                "game_no": self.object.game_no,
                "unit": self.object.unit,
            }
            return redirect("dracogate:unit_confirm", kwargs=kwargs)

    @staticmethod
    def redirect_to_morph_creation(dispatch):
        """
        """
        def new_dispatch(self, request, **kwds):
            """
            """
            if request.user.is_authenticated is True and self.object.owner != request.user:
                kwargs = {
                    "game_no": self.object.game_no,
                    "unit": self.object.unit,
                }
                return redirect("dracogate:unit_confirm", kwargs=kwargs)
            return dispatch(self, request, **kwds)
        return new_dispatch

    #func = decorator(func)

class FilterByUserMixin:
    """
    """

    def get_queryset(self, **kwds):
        """
        """
        owner = (None if self.request.user.is_authenticated is False else self.request.user)
        return super().get_queryset().filter(owner=owner)

# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
