from django.contrib import admin

# Register your models here.
from products.models import Product, ProductCategory, Basket


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity']



@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', 'product' ]