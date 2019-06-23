import datetime
import uuid
from typing import Iterable

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import random


class UserQuerySet(models.QuerySet):
    def delete(self):
        self.update(deleted_at=datetime.datetime.now())


class CommerceUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not phone_number:
            raise ValueError('The given username must be set')
        phone_number = self.model.normalize_username(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)\
            .filter(deleted_at=None)

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = '회원'
        verbose_name_plural = verbose_name

    USERNAME_FIELD = 'username'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=15,
        unique=True
    )
    email = models.EmailField(
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    cart_items = models.ManyToManyField(
        'ProductOption',
        verbose_name='장바구니',
        related_name='users',
        blank=True
    )
    objects = CommerceUserManager()

    def delete(self, **kwargs):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def to_dict(self, fields: Iterable = None):
        if not fields:
            fields = {'id', 'name', 'phone_number'}
        user_dict = {f: getattr(self, f) for f in fields}
        return user_dict

    def set_password(self, password):
        if password:
            super().set_password(password)

        return self

    def set_random_username(self):
        while True:
            username = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(10)])
            if not User.objects.filter(username=username).exists():
                self.username = username
                break

    def __str__(self):
        return f'{self.phone_number}/{self.username}'


class UserSession(models.Model):
    class Meta:
        verbose_name = '유저 세션'
        verbose_name_plural = verbose_name

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    session = models.ForeignKey(
        Session,
        null=True,
        on_delete=models.SET_NULL,
    )
