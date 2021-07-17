from django.urls import path

from .views import (
    site_privacy_rules,)


app_name = 'info'
urlpatterns = [
    path('site-privacy', site_privacy_rules, name='site_privacy'),
]
