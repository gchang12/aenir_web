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

def validate_history(history):
    """
    """
    for method, kwargs in history:
        logger.info("%s(**%r)", method, kwargs)

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
        #validators=[validate_game_no],
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
            logger.info("%s(**%r)", method, kwargs)
            getattr(morph, method)(**kwargs)
        return morph

