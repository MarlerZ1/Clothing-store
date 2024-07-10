from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegistrationForm, UserLoginForm
from users.models import User
from django.test import Client
from django.contrib import auth
# Create your tests here.

class UserLoginViewTestCase(TestCase):
    fixtures = ['socialapp.json']
    def setUp(self):
        self.path = reverse('users:login')

        context = {
            'first_name': 'Kirill',
            'last_name': 'Merzlyakov',
            'username': 'asdsa',
            'email': 'fffff@yandex.ru',
            'password': '12345678QqQqQ'
        }
        User.objects.create_user(
            first_name=context['first_name'],
            last_name=context['last_name'],
            username=context['username'],
            email=context['email'],
            password=context['password']
        )


        self.data = {
            'username': context['username'],
            'password': context['password']
        }


    def test_user_login_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEquals(response.context_data['title'], 'Store - Авторизация')
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context['form'], UserLoginForm)
    def test_user_login_post_success(self):
        response = self.client.post(self.path, self.data)

        self.assertRedirects(response, reverse('index'))

    def test_user_login_post_error(self):
        response = self.client.post(self.path, {'username': 's', 'password': '2'})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')

        self.data = {
            'first_name': 'Kirill',
            'last_name': 'Merzlyakov',
            'username': 'asdsa',
            'email': 'fffff@yandex.ru',
            'password1': '12345678QqQqQ',
            'password2': '12345678QqQqQ'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')
        assert isinstance(response.context_data['form'], UserRegistrationForm)

    def test_user_registration_success(self):

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)



        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_user_registration_error(self):
        username = self.data['username']
        user = User.objects.create(username=username)

        response = self.client.post(self.path, self.data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:profile')

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
    def test_user_profile_get_login(self):
        self.client.login(username=self.context['username'], password=self.context['password'])

        response = self.client.get(self.path)

        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEquals(response.context_data['title'], 'Store - Профиль')
        self.assertIn('form', response.context)
        self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_user_profile_get_unlogin(self):
        response = self.client.get(self.path)

        assert reverse('users:login') in response.url
        self.assertEquals(response.status_code, HTTPStatus.FOUND)

class UserLogoutViewTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:logout')

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
    def test_user_logout_success(self):

        self.assertTrue(self.client.login(username=self.context['username'], password=self.context['password']))


        self.client.post(self.path, {})
        user = auth.get_user(self.client)

        self.assertFalse(user.is_authenticated)