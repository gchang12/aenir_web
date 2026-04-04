"""
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StatBundle:
    """
    """

    def __init__(self, id: str, current_val: int, growth_rate: int | None, max_val: int, absmax_val: int):
        """
        """
        self.id = id
        self.current_val = current_val / 100
        self.growth_rate = growth_rate
        self.max_val = max_val / 100
        self.absmax_val = absmax_val / 100

class VirtualMorph(models.Model):
    """
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
    )
    creation_date = models.DateField(
        auto_now_add=True,
    )
    morph_id = models.CharField(
        max_length=25,
    )
    game_no = models.PositiveSmallIntegerField()
    name = models.CharField(
        max_length=9,
    )
    options = models.JSONField(
        default=dict,
        blank=True,
    )
    history = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta:
        """
        """
        unique_together = [
            ["owner", "morph_id"],
        ]
