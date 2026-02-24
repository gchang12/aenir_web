"""
"""

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from aenir.morph import Morph as VirtualMorph
from aenir import get_morph

User = get_user_model()

def validate_game_no(game_no):
    """
    """
    if game_no not in range(4, 10):
        raise ValidationError(
            "No support for FE%(game_no)d yet.",
            params={"game_no": game_no},
        )

def validate_options(options):
    """
    """
    valid_options = (
        "father",
        "hard_mode",
        "number_of_declines",
        "route",
        "lyn_mode",
    )
    invalid_options = sorted(lambda item: tuple(options).index(item), set(options) - set(valid_options))
    if invalid_options:
        raise ValidationError(
            _("Invalid options were found: %(invalid_options)s."),
            params={"invalid_options": invalid_options},
        )
    for option in set.intersection(valid_options, options):
        if option == "father" and options[option] not in (
            'Arden',
            'Azel',
            'Alec',
            'Claude',
            'Jamka',
            'Dew',
            'Noish',
            'Fin',
            'Beowolf',
            'Holyn',
            'Midayle',
            'Levin',
            'Lex',
       ):
            raise ValidationError(
                _("Invalid 'father' found: '%(father)s'."),
                params={"father": options[option]},
            )
        if option in ("hard_mode", "lyn_mode") and options[option] not in ('true', 'false'):
            raise ValidationError(
                _("Non-pseudo-boolean value found for '%(mode)s': '%(nonboolean)s'."),
                params={"mode": option, "nonboolean": options[option]},
            )
        if option == "number_of_declines" and options[option] not in (str(i) for i in range(0, 4)):
            raise ValidationError(
                _("Invalid 'number_of_declines' value found: '%(number_of_declines)s.'"),
                params={"number_of_declines": options[option]},
            )
        if route == "route" and options[option] not in ("Elphin", "Lalum"):
            raise ValidationError(
                _("Invalid 'route' value found: %(route)s."),
                params={"route": options[option]},
            )

def validate_history(history):
    """
    """
    # check that it's a list of [str, [...args]] pairs
    # also, validate each entry.
    # level_up, promote, use_stat_booster, use_afas_drops, etc.
    try:
        for method, kwargs in history:
            assert isinstance(method, str)
            assert isinstance(kwargs, dict)
            for key in kwargs:
                assert isinstance(key, str)
    except AssertionError as err:
        raise ValidationError(
            "History is invalid",
        )

class Morph(models.Model):
    """
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    # meta: composite pk
    morph_id = models.CharField(
        #min_length=1,
        max_length=25,
        # For forms only
        #blank=False,
        #null=False,
        #validators=[validate_morph_id],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    # content
    game_no = models.PositiveSmallIntegerField(
        validators=[validate_game_no],
    )
    name = models.CharField(
        max_length=9,
        blank=False,
    )
    options = models.JSONField(
        #validators=[validate_options],
        default=dict,
        blank=True,
    )
    history = models.JSONField(
        default=list,
        #validators=[validate_history],
        blank=True,
    )

    class Meta:
        unique_together = [
            ["user", "morph_id"],
        ]

    def recreate(self) -> VirtualMorph:
        """
        """
        game_no = self.game_no
        name = self.name
        options = self.options
        morph = get_morph(game_no, name, **options)
        for method, kwargs in self.history:
            getattr(morph, method)(**kwargs)
        return morph

