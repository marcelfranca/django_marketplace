from django.contrib import admin

# Register your models here.
from .models import Product, Thumbnail


class ThumbnailInline(admin.TabularInline):
    extra = 1
    # prepopulated_fields = {}
    model = Thumbnail


class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "description", "price", "sale_price"]
    search_fields = ["title", "description"]
    list_filter = ["price"]
    list_editable = ["sale_price"]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

admin.site.register(Thumbnail)
