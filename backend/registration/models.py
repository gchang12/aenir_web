"""
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
)

class User(AbstractBaseUser):
    """
    """
    first_name = None
    last_name = None
    email = models.EmailField(
        unique=True,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    #USERNAME_FIELD = "username"
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    #REQUIRED_FIELDS = ["email"]#, "username", "password"]

