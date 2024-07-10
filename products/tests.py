from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from products.models import Product
# Create your tests here.



class IndexViewTestCase(TestCase):
    fixtures = ['products', 'categories']
    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Главная')
        self.assertTemplateUsed(response, 'products\index.html')

class ProductsListViewTestCase(TestCase):
    fixtures = ['products.json', 'categories.json']
    def setUp(self):
        path = reverse('products:index')
        self.response = self.client.get(path)

    def test_list(self):
        products = Product.objects.all()

        self.assertQuerysetEqual(self.response.context_data['object_list'], products[:3], ordered=False)

    def test_view(self):
        self.assertEquals(self.response.status_code, HTTPStatus.OK)
        self.assertEquals(self.response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(self.response, 'products\products.html')