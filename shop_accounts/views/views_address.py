"""
shop_accounts -> views -> user address methods
"""
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from shop_settings.models import City
from tinakala.utils import profile_completion_required

from shop_accounts.models import (
    UserProfile,
    UserAddress,
)
from shop_accounts.forms import (
    UserAddressForm,
)

"""
shop_accounts -> profile address load/create methods
"""


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_address(request):
    address_form = UserAddressForm(request.POST or None, request=request)
    active_addresses: UserAddress = UserAddress.objects.filter(user_id=request.user.id, is_active=True)
    if address_form.is_valid():
        user_new_address = UserAddress.objects.create(
            user=request.user,
            fullname=address_form.cleaned_data.get('fullname'),
            phone=address_form.cleaned_data.get('phone'),
            state=address_form.cleaned_data.get('state'),
            city=address_form.cleaned_data.get('city'),
            address=address_form.cleaned_data.get('address'),
            postal_code=address_form.cleaned_data.get('postal_code'),
            plaque=address_form.cleaned_data.get('plaque'),
        )
        user_new_address.save()
        address_form = UserAddressForm()
        messages.success(request, 'آدرس شما با موفقیت ثبت شد.')
        return redirect('auth:user-address')
    context = {
        'active_addresses': active_addresses,
        'address_form': address_form,
    }
    return render(request, 'accounts/SiteAddress.html', context)


@require_http_methods(['GET', ])
@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_get_cities_of_state(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).order_by('city').values()
    return JsonResponse(list(cities), safe=False)


"""
shop_accounts -> profile address updating methods
"""


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_address_detail(request, address_id):
    address: UserAddress = get_object_or_404(klass=UserAddress, pk=address_id, is_active=True, user=request.user)
    address_form = UserAddressForm(request.POST or None, request=request, initial={
        'fullname': address.fullname,
        'phone': address.phone,
        'state': address.state,
        'city': address.city,
        'address': address.address,
        'postal_code': address.postal_code,
        'plaque': address.plaque,
    })
    if address_form.is_valid():
        address.fullname = address_form.cleaned_data.get('fullname')
        address.phone = address_form.cleaned_data.get('phone')
        address.state = address_form.cleaned_data.get('state')
        address.city = address_form.cleaned_data.get('city')
        address.address = address_form.cleaned_data.get('address')
        address.postal_code = address_form.cleaned_data.get('postal_code')
        address.plaque = address_form.cleaned_data.get('plaque')
        address.is_active = True
        address.save()
        messages.success(request, 'بروزرسانی آدرس با موفقیت انجام شد.')
        return redirect('auth:user-address')
    context = {
        'address_id': address.id,
        'address_form': address_form,
    }
    return render(request, 'accounts/SiteAddressDetail.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_address_delete(request, address_id):
    address: UserAddress = get_object_or_404(klass=UserAddress, pk=address_id)
    if address.user != request.user:
        return Http404('آدرسی با این مشخصات برای شما وجود ندارد.')
    address.is_active = False
    address.save()
    messages.success(request, 'آدرس شما با موفقیت حذف شد.')
    return redirect('auth:user-address')
