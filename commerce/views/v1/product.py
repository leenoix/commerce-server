from commerce.models import Product
from commerce.views import JsonView


class ProductView(JsonView):
    def get(self, request):
        return {
            'code': 'success',
            'data': [p.to_dict()
                     for p in Product.objects.filter(deleted_at=None, is_active=True).order_by('provider')]
        }