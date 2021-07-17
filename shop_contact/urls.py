from django.urls import path

from .views import contact_us

app_name = 'contact'
urlpatterns = [
    path('contact-us', contact_us, name='contact-us'),
]
