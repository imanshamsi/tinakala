
"""tinakala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .settings import (
    DEBUG,
    STATIC_URL,
    STATIC_ROOT,
    MEDIA_URL,
    MEDIA_ROOT,
)
from .views import (
    home_page,
)

urlpatterns = [
    # reset password urls
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/reset_password/password_reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/reset_password/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/reset_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='accounts/reset_password/password_reset_complete.html'), name='password_reset_complete'),
    # admin panel urls
    path('admin/', admin.site.urls),
    # ckeditor path
    url(r'^ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
    # main application urls
    path('', home_page, name='home-page'),
    path('', include('shop_accounts.urls', namespace='auth')),
    path('', include('shop_settings.urls', namespace='info')),
    path('', include('shop_contact.urls', namespace='contact')),
    path('blog/', include('shop_blog.urls', namespace='blog')),
    path('products/', include('shop_products.urls', namespace='products')),
    path('cart/', include('shop_cart.urls', namespace='cart')),
    path('order/', include('shop_order.urls', namespace='order')),
]
if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
