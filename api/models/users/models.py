from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from core.models import TimeStampedModel
from api.models.users.managers import UserManager


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=15, unique=True, blank=True, null=True)

    is_active = models.BooleanField("active", default=True)
    is_staff = models.BooleanField("is_staff", default=False)
    is_superuser = models.BooleanField("is_superuser", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
