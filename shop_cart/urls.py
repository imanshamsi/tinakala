from django.urls import path

from shop_cart.views import *

app_name = 'cart'
urlpatterns = [
    path('', cart_view, name='user-cart'),
    path('add/<str:product_code>', cart_add, name='user-cart-add'),
    path('remove/<str:product_code>', cart_remove, name='user-cart-remove'),
]
