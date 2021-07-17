from django.urls import path

from shop_order.views import *

app_name = 'order'
urlpatterns = [
    path('check-out', cart_check_out, name='check-out'),
    path('to-bank/<str:order_code>/', to_bank, name='to-bank'),
    path('call-back', call_back, name='call-back'),
]
