from django.contrib.gis import admin

from commerce.models import ProductOption


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    pass
