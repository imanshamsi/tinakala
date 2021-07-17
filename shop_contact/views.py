import datetime

from django.shortcuts import render
from django.contrib import messages

from .forms import ContactUsForm
from .models import Ticket


def contact_us(request):
    contact_form = ContactUsForm(request.POST or None)
    if contact_form.is_valid():
        Ticket.objects.create(
            fullname=contact_form.cleaned_data.get('fullname'),
            phone=contact_form.cleaned_data.get('phone'),
            email=contact_form.cleaned_data.get('email'),
            title=contact_form.cleaned_data.get('title'),
            content=contact_form.cleaned_data.get('content'),
            created_at=datetime.datetime.now(),
        )
        messages.success(request, 'پیام شما با موفقیت ارسال شد')
        contact_form = ContactUsForm()
    context = {
        'contact_form': contact_form,
    }
    return render(request, 'contact/SiteContactUs.html', context)
