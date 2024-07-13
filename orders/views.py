from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView

from common.views import TitleMixin
from orders.forms import OrderForm

import stripe

from orders.models import Order
from products.models import Basket
from store_server import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class OrderCreateView(LoginRequiredMixin, TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_success')

    def post(self, request, *args, **kwargs):
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


class SuccessTemplateView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CancelTemplateView(LoginRequiredMixin, TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'
    title = 'Store - Заказ отменен'

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