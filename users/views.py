from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User


# Create your views here.

class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy("index")

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'Store - Регистрация'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно зарегестрированы!')
        return response


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Store - Профиль'
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context



class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("index")
