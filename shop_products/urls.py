from django.urls import path

from .views import (
    search_products_view,
    get_product_amazing,
    detail_product_view,
    get_product_by_brand_view,
    search_product_by_category_view,
)

app_name = 'products'
urlpatterns = [
    path('search/', search_products_view, name='search'),
    path('search/suggested/', get_product_amazing, name='suggested'),
    path('search/<category>', search_product_by_category_view, name='search_by_category'),
    path('search/brand/<brand>', get_product_by_brand_view, name='product_by_brand'),
    path('<product_code>/<product_slug>', detail_product_view, name='detail_product'),
]
