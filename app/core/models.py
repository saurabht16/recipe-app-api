from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                PermissionsMixin


class UserManager(BaseUserManager):
    """
    Class for custom user manager
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and saves new user
        :param email: Email Field
        :param password: Password Field
        :param extra_fields: **kwargs argument for any extra field
        :return: new user
        """
        if not email:
            raise ValueError("User must have a Valid email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Create and saves new superuser
        :param email: Email Field
        :param password: Password Field
        :return: new superuser
        """
        superuser = self.create_user(email, password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user Model Class that supports using email instead of username
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
