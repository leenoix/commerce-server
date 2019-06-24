from django.db import transaction
from django.db.models import Sum, Min

from commerce.models import ProductOption
from commerce.views import JsonView


class PurchaseView(JsonView):
    LOGIN_REQUIRED = True
    REQUIRED_FIELDS = ('option_ids',)

    def post(self, request):
        return {
            'code': 'success',
            'total_price': self.get_total_price(request.POST['option_ids']),
        }

    @transaction.atomic
    def patch(self, request):
        options = ProductOption.objects.filter(id__in=request.PATCH['option_ids'], deleted_at=None, stock__gt=0)
        for option in options:
            option.stock -= 1
            option.save()

        purchase = request.user.purchases.create(
            user=request.user,
            paid_price=self.get_total_price(request.PATCH['option_ids'])
        )

        for option in options:
            purchase.rows.create(option=option, amount=1)

        return {
            'code': 'success',
            'purchase_id': purchase.id,
            'purchase_list': [
                r.option.to_dict(with_product_info=True) for r in purchase.rows.all()
            ],
            'total_price': purchase.paid_price,
        }

    def get_total_price(self, option_ids):
        options = ProductOption.objects.filter(id__in=option_ids, deleted_at=None, stock__gt=0)

        total_price = options.aggregate(total=Sum('product__price'))['total'] or 0

        for provider in ProductOption.objects.all().distinct('product__provider').values('product__provider'):
            provider = provider['product__provider']
            total_price += options.filter(
                product__provider=provider, product__can_bundle=False
            ).aggregate(total=Sum('product__shipping_price'))['total'] or 0
            total_price += options.filter(
                product__provider=provider, product__can_bundle=True
            ).aggregate(min=Min('product__shipping_price'))['min'] or 0

        return total_price
