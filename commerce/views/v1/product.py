from commerce.models import Product, ProductOption
from commerce.views import JsonView


class ProductView(JsonView):
    def get(self, request):
        return {
            'code': 'success',
            'data': [p.to_dict()
                     for p in Product.objects.filter(deleted_at=None, is_active=True).order_by('provider')]
        }


class ShoppingCartView(JsonView):
    LOGIN_REQUIRED = True
    REQUIRED_FIELDS = {
        'POST': ('option_id',)
    }

    def get(self, request):
        return {
            'code': 'success',
            'data': [o.to_dict(with_product_info=True) for o in request.user.cart_items.all()]
        }

    def post(self, request):
        try:
            option = ProductOption.objects.get(id=request.POST['option_id'])
        except Exception:
            return dict(code='OPTION_NOT_FOUND', message='Option is not found'), 400

        request.user.cart_items.add(option)
        return {'code': 'success'}
