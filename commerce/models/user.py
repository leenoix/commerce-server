import datetime
import uuid
from typing import Iterable

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.gis.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import random


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
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

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
