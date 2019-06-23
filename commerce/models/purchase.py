import datetime
import uuid

from django.contrib.gis.db import models

from commerce.models import Provider, ChoiceEnum, User, ProductOption


class PurchaseLog(models.Model):
    class Meta:
        verbose_name = '구매 내역'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.id

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paid_price = models.IntegerField(default=0, verbose_name='결제 금액')
    user = models.ForeignKey(
        User,
        related_name='purchases',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True, verbose_name='주문 요청 사항')

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save()


class PurchaseRow(models.Model):
    class Meta:
        verbose_name = '구매 정보'
        verbose_name_plural = verbose_name

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.IntegerField(default=0, verbose_name='구매 수량')
    option = models.ForeignKey(
        ProductOption,
        related_name='purchase_rows',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    purchase = models.ForeignKey(
        PurchaseLog,
        related_name='rows',
        on_delete=models.CASCADE,
    )
