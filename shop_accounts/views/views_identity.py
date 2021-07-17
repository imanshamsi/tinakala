"""
shop_accounts -> views -> authentication methods
"""
import random
import string
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from tinakala.utils import profile_completion_required

from shop_accounts.models import (
    UserProfile,
)
from shop_accounts.forms import (
    LoginForm,
    RegisterForm,
    ChangePasswordForm,
)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username_email = login_form.cleaned_data.get('username_email')
        login_query = (
                Q(username__iexact=username_email) |
                Q(email__iexact=username_email)
        )
        username: User = User.objects.filter(login_query).first()
        if username:
            password = login_form.cleaned_data.get('password')
            remember_me = login_form.cleaned_data.get('remember_me')
            user = authenticate(request, username=username.username, password=password)
            if user is not None:
                login(request, user)
                # user login -> remember me
                if not remember_me:
                    request.session.set_expiry(0)
                # check user profile completion
                is_profile_completed: UserProfile = UserProfile.objects.get(user_id=request.user.id).done
                if is_profile_completed:
                    messages.add_message(request, messages.INFO,
                                         f'کاربر {request.user.get_full_name()} عزیز به تیناکالا خوش آمدی')
                    if request.GET.get('next'):
                        return redirect(request.GET.get('next'))
                    return redirect('home-page')
                else:
                    return redirect('auth:change-profile')
            else:
                login_form.add_error('username_email', 'کاربری با این مشخصات یافت نشد!')
        else:
            login_form.add_error('username_email', 'کاربری با این مشخصات یافت نشد!')
    context = {
        'login_form': login_form,
    }

    return render(request, 'accounts/SiteLogin.html', context)


@login_required(login_url='auth:login')
def logout_user(request):
    logout(request)
    return redirect('home-page')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        email = register_form.cleaned_data.get('email')
        random_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        username = f'user_{random_string}_{random.randint(10000000, 99999999)}'
        password = register_form.cleaned_data.get('password')
        user_created = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user_created, birth_day=datetime.today())
        messages.add_message(request, messages.INFO, 'خوش آمدید، حساب کاربری شما با موفقیت ایجاد شد.')
        return redirect('auth:login')
    context = {
        'register_form': register_form,
    }
    return render(request, 'accounts/SiteRegister.html', context)


@login_required(login_url='auth:login')
@profile_completion_required(profile_model=UserProfile, redirected_path='auth:change-profile')
def user_reset_password(request):
    reset_password_form = ChangePasswordForm(request.POST or None, user=request.user)
    if reset_password_form.is_valid():
        new_password = reset_password_form.cleaned_data.get('new_password')
        user = User.objects.get(pk=request.user.id)
        user.set_password(new_password)
        user.save()
        logout(request)
        messages.add_message(request, messages.INFO, 'رمز عبور شما با موفقیت تغییر یافت!')
        return redirect('auth:login')
    context = {
        'reset_password_form': reset_password_form,
    }
    return render(request, 'accounts/SiteResetPassword.html', context)
