from django.contrib import admin

from store.models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_stock', 'created_date', 'last_modified')
    prepopulated_fields = {'product_slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)
