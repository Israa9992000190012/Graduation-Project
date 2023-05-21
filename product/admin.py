from django.contrib import admin
from .models import Product, Material, ProductMaterial

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_cat')
    list_filter = ('product_cat', 'product_price')
    search_fields = ('product_name', 'product_cat', 'product_price')

admin.site.register(Product, ProductAdmin)
admin.site.register(Material)
admin.site.register(ProductMaterial)