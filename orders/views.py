from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from common.views import TitleMixin
from orders.forms import OrderForm


# Create your views here.
class OrderCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)