"""
"""

from django.db import models
from django.contrib.auth.models import (
    #AbstractBaseUser,
    AbstractUser,
    UserManager,
    #User,
)

class User(AbstractUser):
    """
    """
    email = models.EmailField(
        unique=True,
    )
    username = models.CharField(
        max_length=26,
        unique=True,
    )
    first_name = None
    last_name = None
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_superuser = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
