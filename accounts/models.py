"""
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

from ._logging import logger

# Create your models here.

class User(AbstractUser):
    """
    """
    first_name = None
    last_name = None
