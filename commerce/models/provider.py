import uuid

from django.contrib.gis.db import models

__all__ = 'Provider',


class Provider(models.Model):
    class Meta:
        verbose_name = '공급자'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='공급자명')
    address = models.CharField(max_length=300, verbose_name='주소', null=True, blank=True)
    phone_number = models.CharField(max_length=20, verbose_name='전화번호', null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)