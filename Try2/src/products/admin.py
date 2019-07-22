from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "description", "price", "sale_price"]
    search_fields = ["title", "description", "price"]
    list_filter = ["price", "title"]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
