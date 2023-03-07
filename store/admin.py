from django.contrib import admin

from store.models import Product, Variation


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_stock', 'created_date', 'last_modified')
    prepopulated_fields = {'product_slug': ('product_name',)}


class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value', 'is_active')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationsAdmin)
