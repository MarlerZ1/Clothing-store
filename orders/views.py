from http import HTTPStatus

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _, gettext
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket
from store_server import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class OrderCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = _('Store - Оформление заказа')
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_success')

    def post(self, request, *args, **kwargs):
        last_order = Order.objects.filter(initiator=self.request.user).last()
        if last_order and last_order.status == 0:
            last_order.delete()

        super(OrderCreateView, self).post(self, request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=settings.DOMAIN_NAME + reverse('orders:order_success'),
            cancel_url=settings.DOMAIN_NAME + reverse('orders:order_canceled'),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = _('Store - Заказы')
    model = Order
    ordering = ('-created',)

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Store - {gettext("Заказ")} #{self.object.id}'
        return context


class SuccessTemplateView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = _('Store - Спасибо за заказ!')


class CancelTemplateView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = _('Store - Заказ отменен')


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object'])

    return HttpResponse(status=200)


def fulfill_checkout(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
