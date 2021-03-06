import datetime

from django.contrib.gis.db import models

from commerce.models import Provider, ChoiceEnum


class Product(models.Model):
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = verbose_name

    class ShippingChoice(ChoiceEnum):
        PREPAY = '선결제'
        FREE = '무료'

    def __str__(self):
        return self.name

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='상품명')
    price = models.IntegerField(default=0, verbose_name='가격')
    image = models.ImageField(
        null=True,
        blank=True,
        max_length=500,
        upload_to='product_image'
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='판매 중')
    provider = models.ForeignKey(
        Provider,
        related_name='products',
        on_delete=models.CASCADE,
    )
    description = models.TextField(null=True, blank=True)
    shipping_method = models.CharField(
        max_length=7,
        choices=ShippingChoice.choices(),
        default=ShippingChoice.FREE.name
    )
    shipping_price = models.IntegerField(default=0, verbose_name='배송비')
    can_bundle = models.BooleanField(default=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image.url if self.image else '',
            'provider': self.provider.name,
            'description': self.description,
            'shipping_method': self.shipping_method,
            'shipping_price': self.shipping_price,
            'can_bundle': self.can_bundle,
            'options': [o.to_dict() for o in self.options.filter(deleted_at=None)]
        }


class ProductOption(models.Model):
    class Meta:
        verbose_name = '상품옵션'
        verbose_name_plural = verbose_name

    class SizeChoice(ChoiceEnum):
        S = '소'
        M = '중'
        L = '대'
        XL = '특대'

    def __str__(self):
        return str(self.id)

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        Product,
        related_name='options',
        on_delete=models.CASCADE,
    )
    stock = models.IntegerField(default=0, verbose_name='재고')
    deleted_at = models.DateTimeField(null=True, blank=True)
    size = models.CharField(
        max_length=3,
        choices=SizeChoice.choices(),
        default=SizeChoice.M.name
    )
    color = models.CharField(
        max_length=30,
        verbose_name='색상',
        default='white'
    )

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.datetime.now()
        self.save()

    def to_dict(self, with_product_info=False):
        _dict = {
            'id': self.id,
            'stock': self.stock,
            'size': self.size,
            'color': self.color,
        }
        if with_product_info:
            product = self.product
            _dict['name'] = product.name
            _dict['price'] = product.price
            _dict['image'] = product.image.url if product.image else ''
            _dict['provider'] = product.provider.name
        return _dict
