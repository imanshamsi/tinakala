"""
shop_accounts -> views -> user profile methods
"""
from datetime import datetime, timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from tinakala.utils import get_random_otp, send_otp
from tinakala.utils import profile_completion_required

from shop_settings.models import SiteSetting
from shop_accounts.models import (
    UserProfile, UserFavorite,
)
from shop_accounts.forms import (
    ChangeUserProfileForm,
    ChangeUserAvatarForm,
    VerifyPhoneForm,
)

"""
shop_accounts -> profile info loading methods
"""


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_profile(request):
    context = {}
    return render(request, 'accounts/SiteUserProfile.html', context)


@login_required(login_url='auth:login')
def user_profile_info(request):
    user: UserProfile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'accounts/component/profile_user_info.html', context)


@login_required(login_url='auth:login')
def user_profile_favourite(request):
    favorites = get_object_or_404(UserFavorite, user=request.user).product.all()[:3]
    context = {
        'favorites': favorites,
    }
    return render(request, 'accounts/component/profile_user_favorite.html', context)


@login_required(login_url='auth:login')
def user_profile_panel(request):
    user: UserProfile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'user': user,
    }
    return render(request, 'accounts/component/profile_user_panel.html', context)


@login_required(login_url='auth:login')
def user_profile_sidebar_menu(request):
    context = {}
    return render(request, 'accounts/component/profile_user_sidebar_menu.html', context)


"""
shop_accounts -> profile info updating methods
"""


@login_required(login_url='auth:login')
def user_change_profile(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    change_profile_form = ChangeUserProfileForm(request.POST or None, initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': profile.phone,
        'gender': profile.gender,
        'national_code': profile.national_code,
        'birth_day': profile.birth_day,
    })
    change_avatar_form = ChangeUserAvatarForm(request.POST or None, request.FILES or None)
    if change_profile_form.is_valid() and change_avatar_form.is_valid():
        user: User = User.objects.get(pk=request.user.id)
        user.first_name = change_profile_form.cleaned_data.get('first_name')
        user.last_name = change_profile_form.cleaned_data.get('last_name')
        # start phone-verify False if phone changed
        new_profile_phone = change_profile_form.cleaned_data.get('phone')
        if profile.phone != new_profile_phone:
            profile.phone = change_profile_form.cleaned_data.get('phone')
            profile.phone_verify = False
        # end phone-verify False if phone changed
        profile.gender = change_profile_form.cleaned_data.get('gender')
        profile.national_code = change_profile_form.cleaned_data.get('national_code')
        profile.birth_day = change_profile_form.cleaned_data.get('birth_day')
        new_profile_avatar = change_avatar_form.cleaned_data.get('avatar')
        if new_profile_avatar:
            profile.avatar = change_avatar_form.cleaned_data.get('avatar')
        profile.done = True
        user.save()
        profile.save()
        messages.add_message(request, messages.INFO, 'اطلاعات کاربری شما با موفقیت تغییر یافت!')
        return redirect('auth:user-profile')
    context = {
        'change_profile_form': change_profile_form,
        'change_avatar_form': change_avatar_form,
        'profile_done': profile.done,
        'profile_current_avatar': profile.avatar,
    }
    return render(request, 'accounts/SiteChangeProfile.html', context)


"""
shop_accounts -> profile phone verify methods
"""


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_send_otp(request):
    user: UserProfile = UserProfile.objects.get(user_id=request.user.id)
    otp = get_random_otp()
    if user.otp:
        otp_timeout = datetime.now(timezone.utc) - user.otp_generated_date
        if otp_timeout.days == 0 and otp_timeout.seconds < 120:
            messages.add_message(
                request,
                messages.INFO,
                f'برای حساب شما کد فعال وجود دارد. برای درخواست جدید {120 - otp_timeout.seconds} ثانیه صبر کنید'
            )
            return redirect('auth:verify-phone')
    sms_message: SiteSetting = SiteSetting.objects.all().first().sms_message
    send_otp(user.phone, otp, message=sms_message)
    user.otp = otp
    user.otp_generated_date = datetime.now()
    user.save()
    messages.add_message(request, messages.INFO, f'کد تایید برای شماره همراه {user.phone} ارسال شد')
    return redirect('auth:verify-phone')


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_verify_phone(request):
    user: UserProfile = UserProfile.objects.get(user_id=request.user.id)
    if user.phone_verify:
        return redirect('auth:user-profile')
    verify_phone_form = VerifyPhoneForm(request.POST or None, request=request)
    if verify_phone_form.is_valid():
        entered_code = verify_phone_form.cleaned_data.get('fifth_char')
        if entered_code == user.otp:
            user.phone_verify = True
            user.save()
            messages.add_message(request, messages.INFO, 'شماره همراه با موفقیت تایید شد!')
            return redirect('auth:user-profile')
    context = {
        'user_phone': user.phone,
        'verify_phone_form': verify_phone_form,
    }
    return render(request, 'accounts/SiteVerifyPhone.html', context)
