from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from orders.forms import OrderForm
from orders.models import Order
from users.models import User


# Create your tests here.

class OrderCreateViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('orders:order_create')

        self.context = {
            'first_name': 'Kirill',
            'last_name': 'Merzlyakov',
            'username': 'asdsa',
            'email': 'fffff@yandex.ru',
            'password': '12345678QqQqQ'
        }
        User.objects.create_user(
            first_name=self.context['first_name'],
            last_name=self.context['last_name'],
            username=self.context['username'],
            email=self.context['email'],
            password=self.context['password']
        )

    def test_order_create_view_get_authorized(self):
        self.client.login(username=self.context['username'], password=self.context['password'])

        response = self.client.get(self.path)


        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('orders/order-create.html')
        self.assertEquals(response.context_data['title'], 'Store - Оформление заказа')
        self.assertIn('form', response.context_data)
        self.assertTrue(isinstance(response.context_data['form'], OrderForm))

    def test_order_create_view_get_unauthorized(self):
        response = self.client.get(self.path)

        assert reverse('users:login') in response.url
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
    def test_order_create_view_post(self):
        self.client.login(username=self.context['username'], password=self.context['password'])

        response = self.client.post(self.path, first_name=self.context['first_name'], last_name=self.context['last_name'],
                                    email=self.context['email'], address='Address home 1234')

        self.assertTrue(Order.objects.all().exists())
        self.assertRedirects(response, reverse('orders:success'), fetch_redirect_response=False)