from django.contrib.gis import admin

from commerce.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
