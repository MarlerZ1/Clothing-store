from django.contrib import admin

# Register your models here.
from products.models import Product, ProductCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']
    fields = ['name', 'price', 'quantity']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    fields = ['name',]