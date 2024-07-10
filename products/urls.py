from django.urls import path
from products.views import ProductsListView, basket_add, basket_remove
from django.views.decorators.cache import cache_page
app_name = 'products'

urlpatterns = [
    path('', cache_page(90)(ProductsListView.as_view()), name="index"),
    path('category/<int:category_id>', cache_page(90)(ProductsListView.as_view()), name="category"),
    path('category/<int:category_id>/<int:page>', cache_page(90)(ProductsListView.as_view()), name="category_paginator"),
    path('page/<int:page>', cache_page(90)(ProductsListView.as_view()), name="paginator"),
    path('baskets/add/<int:product_id>', basket_add, name="basket_add"),
    path('baskets/remove/<int:basket_id>', basket_remove, name="basket_remove"),
]