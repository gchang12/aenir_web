"""
"""

# TODO: Handle game-exclusive methods
# TODO: Forbid user from invoking methods that are invalid in a given Morph class.
# TODO: Make sure user can see and access only his own VirtualMorph objects.

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
        # forbid users who don't own objects from interacting with vmorph.
        # anon-user selects owned morph
        if (self.object.owner is not None) and (owner is None):
            # redirect to create new morph page?
            # redirect to login page?
            raise Http403
        # forbid bad methods.
        # user selects morph he does not own.
        if (self.object.owner is not None) and (self.object.owner != owner):
            # redirect to morph list
            # prompt user to create morph
        return super().dispatch(request, **kwds)

class ForbidForbiddenMethodMixin:
    """
    """

    def dispatch(self, request, **kwds):
        """
        """
        owner = (None if self.request.user.is_authenticated is False else self.request.user)
        # forbid users who don't own objects from interacting with vmorph.
        # anon-user selects owned morph
        if (self.object.owner is not None) and (owner is None):
            # redirect to create new morph page?
            # redirect to login page?
            raise Http403
        # forbid bad methods.
        # user selects morph he does not own.
        if (self.object.owner is not None) and (self.object.owner != owner):
            # redirect to morph list
            # prompt user to create morph
        if self.object.game_no not in self.valid_games:
            raise Http400
        return super().dispatch(request, **kwds)

# TODO: In case user selects a morph he does not own
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


# TODO: In case user is not logged in and selects a morph that is not owned.
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

# TODO: In case user is logged in and accesses a morph not owned by him (SHOULD NOT HAPPEN!)
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

class GetUserObjectsOnlyMixin:
    """
    Retrieves only morphs that belong to user.
    """

    def get_queryset(self, **kwds):
        """
        Returns only user's morphs, ordered by newest to oldest.
        """
        owner = (None if self.request.user.is_authenticated is False else self.request.user)
        queryset = self.model.objects.filter(owner=owner).order_by("-creation_date")
        return queryset

# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4
# TODO: For all: Redirect user to create morph if he does not own morph.
# TODO: Redirect if morph is from FE4

