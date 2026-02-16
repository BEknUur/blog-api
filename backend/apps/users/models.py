from django.db.models import (
    CharField,
    EmailField, 
    BooleanField,
    DateTimeField,
    ImageField,
)
from django.contrib.auth.models import ( 
    AbstractBaseUser, 
    PermissionsMixin, 
    BaseUserManager,
)
from apps.abstract.models import AbstractTimeStampModel

from typing import Any
from apps.users.manager import CustomUserManager



FIRST_NAME_MAX_LENGTH = 50
LAST_NAME_MAX_LENGTH = 50


class CustomUser(
    AbstractBaseUser,
    AbstractTimeStampModel,
    PermissionsMixin
):
    email=EmailField(
        unique=True,
    )
    first_name=CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    
    )
    last_name=CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )
    is_active=BooleanField(
        default=True,
    )
    is_staff=BooleanField(
        default=False,
    )
    data_jonded=DateTimeField(
        auto_now_add=True,
    )
    avatar=ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    
    objects = CustomUserManager()

    class Meta:
        verbose_name="user"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"