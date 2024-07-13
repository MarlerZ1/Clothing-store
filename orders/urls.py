from django.urls import path
from orders.views import OrderCreateView, CancelTemplateView, SuccessTemplateView, OrderListView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('order-create', OrderCreateView.as_view(), name="order_create"),
    path('order-success', SuccessTemplateView.as_view(), name="order_success"),
    path('order-canceled', CancelTemplateView.as_view(), name="order_canceled"),
    path('order/<int:pk>', OrderDetailView.as_view(), name="order"),
    path('', OrderListView.as_view(), name="orders_list"),
]