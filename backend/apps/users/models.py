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

class CustomUserManager(BaseUserManager):
    """
    Docstring for CustomUserManager
    """
    def create_user(
            self,
            email:str, 
            first_name:str, 
            last_name:str, 
            password:str,
            *args:tuple[Any,...],
            **kwargs:dict[Any,Any],
    )->"CustomUser":
        
        """
        Docstring for create_user
        
        :param self: Description
        :param email: Description
        :type email: str
        :param first_name: Description
        :type first_name: str
        :param last_name: Description
        :type last_name: str
        :param password: Description
        :type password: str
        :param args: Description
        :type args: tuple[Any, ...]
        :param kwargs: Description
        :type kwargs: dict[Any, Any]
        :return: Description
        :rtype: Any
        """
        if not email:
            raise ValueError("User must have an email address")
        
        if not password:
            raise ValueError("User must have a password")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name, 
            last_name=last_name,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user 
    


    def create_super_user(
            self,
            email:str, 
            first_name:str, 
            last_name:str, 
            password:str,
            *args:tuple[Any,...],
            **kwargs:dict[Any,Any],
    )->"CustomUser":
        
        """
        Docstring for create_super_user
        
        :param self: Description
        :param email: Description
        :type email: str
        :param first_name: Description
        :type first_name: str
        :param last_name: Description
        :type last_name: str
        :param password: Description
        :type password: str
        :param args: Description
        :type args: tuple[Any, ...]
        :param kwargs: Description
        :type kwargs: dict[Any, Any]
        :return: Description
        :rtype: Any
        """

        if not email:
            raise ValueError("There should be the email")
        
        if not password:
            raise ValueError("There should be the password")
        
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name, 
            last_name=last_name,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self.db)

        return user
    


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