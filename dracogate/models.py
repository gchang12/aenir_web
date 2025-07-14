"""
"""

from django.db import models
from django.contrib.auth import get_user_model

import aenir
import aenir.morph
#help(aenir)

from aenir import (
    Morph4,
    Morph5,
    Morph6,
    Morph7,
    Morph8,
    Morph9,
)

User = get_user_model()

# Create your models here.
# TODO: May not be implementing this very efficiently.

class AbstractMorph(models.Model):
    """
    """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        """
        abstract = True

class Morph4(AbstractMorph, Morph4):
    """
    """

class Morph5(AbstractMorph, Morph5):
    """
    """

class Morph6(AbstractMorph, Morph6):
    """
    """

class Morph7(AbstractMorph, Morph7):
    """
    """

class Morph8(AbstractMorph, Morph8):
    """
    """

class Morph9(AbstractMorph, Morph9):
    """
    """
