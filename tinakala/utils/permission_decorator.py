from django.contrib import messages
from django.shortcuts import redirect


def profile_completion_required(profile_model, redirected_path):
    def check_profile(function):
        def _function(request, *args, **kwargs):
            user = profile_model.objects.get(user_id=request.user.id)
            if not user.done:
                messages.add_message(request, messages.WARNING, 'جهت دسترسی به تمامی قسمت ها نیاز به تکمیل پروفایل است')
                return redirect(redirected_path)
            return function(request, *args, **kwargs)
        return _function
    return check_profile


def verify_phone_required(profile_model, redirected_path):
    def check_phone(function):
        def _function(request, *args, **kwargs):
            user = profile_model.objects.get(user_id=request.user.id)
            if not user.phone_verify:
                messages.add_message(request, messages.WARNING, 'جهت دسترسی به تمامی قسمت ها نیاز به تایید موبایل است')
                return redirect(redirected_path)
            return function(request, *args, **kwargs)
        return _function
    return check_phone
