import re
from datetime import datetime, timezone

from captcha.fields import ReCaptchaField
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from .models import (
    UserProfile,
    State,
    City,
    UserAddress,
)


class LoginForm(forms.Form):
    captcha = ReCaptchaField()
    username_email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'ایمیل یا نام کاربری خود را وارد نمایید',
        }),
        label='ایمیل یا نام کاربری',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'رمز عبور خود را وارد نمایید',
        }),
        label='رمز عبور',
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'custom-control-input',
        }),
        label='مرا به خاطر بسپار',
        required=False,
    )


class RegisterForm(forms.Form):
    captcha = ReCaptchaField()
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'ایمیل خود را وارد نمایید',
        }),
        label='ایمیل',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'رمز عبور خود را وارد نمایید',
        }),
        label='رمز عبور',
    )
    verify_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'رمز عبور خود را مجدد وارد نمایید',
        }),
        label='تکرار رمز عبور',
    )
    agree_rule = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'id': 'customCheck3',
            'class': 'custom-control-input',
            'placeholder': 'رمز عبور خود را مجدد وارد نمایید',
        }),
        label='حریم خصوصی و قوانین استفاده از سرویس های سایت تیناکالا را مطالعه نموده و با کلیه موارد آن موافقم.',
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exist_user_by_email = User.objects.filter(email__iexact=email)
        if is_exist_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده قبلا در سایت ثبت شده است')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email == password:
            raise forms.ValidationError('شما مجاز به استفاده از ایمیل به جای رمز عبور نیستید!')
        if re.search('[A-Z]', password) is None or \
                re.search('[a-z]', password) is None or \
                re.search('[0-9]', password) is None or \
                len(password) < 8:
            raise forms.ValidationError('رمز عبور باید دارای 8 کاراکتر به صورت یک حرف بزرگ ، یک حرف کوچک و اعداد باشد!')
        return password

    def clean_verify_password(self):
        password = self.cleaned_data.get('password')
        verify_password = self.cleaned_data.get('verify_password')
        if password != verify_password:
            raise forms.ValidationError('رمز عبور با تکرار خود تطابق ندارد!')
        return verify_password

    def clean_agree_rule(self):
        agree_rule = self.cleaned_data.get('agree_rule')
        if not agree_rule:
            raise forms.ValidationError('برای ثبت نام باید با حریم خصوصی و قوانین موافقت کرده باشید!')
        return agree_rule


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'رمز عبور خود را وارد کنید',
        }),
        label='رمز عبور قبلی'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'رمز عبور خود را وارد کنید',
        }),
        label='رمز عبور جدید'
    )
    verify_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'رمز عبور خود را وارد کنید',
        }),
        label='تکرار رمز عبور جدید'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if check_password(old_password, self.user.password):
            return old_password
        else:
            raise forms.ValidationError('رمز عبور صحیح نمی باشد!')

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if check_password(new_password, self.user.password):
            raise forms.ValidationError('رمز عبور باید با رمز قبلی شما متفاوت باشد!')
        if new_password == self.user.email:
            raise forms.ValidationError('شما مجاز به استفاده از ایمیل به جای رمز عبور نیستید!')
        if re.search('[A-Z]', new_password) is None or \
                re.search('[a-z]', new_password) is None or \
                re.search('[0-9]', new_password) is None or \
                len(new_password) < 8:
            raise forms.ValidationError('رمز عبور باید دارای 8 کاراکتر به صورت یک حرف بزرگ ، یک حرف کوچک و اعداد باشد!')
        return new_password

    def clean_verify_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        verify_new_password = self.cleaned_data.get('verify_new_password')
        if new_password != verify_new_password:
            raise forms.ValidationError('رمز عبور با تکرار خود تطابق ندارد!')
        return verify_new_password


class ChangeUserProfileForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'نام خود را وارد کنید',
        }),
        label='نام',
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'نام خانوادگی خود را وارد کنید',
        }),
        label='نام خانوادگی',
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'شماره همراه خود را وارد کنید',
        }),
        label='شماره همراه',
    )
    GENDER_CHOICES = (
        (1, 'مرد'),
        (2, 'زن'),
    )
    gender = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'nice-select right',
            # 'style': 'display: none;',
        }),
        label='جنسیت',
        choices=GENDER_CHOICES
    )
    national_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'کد ملی خود را وارد کنید',
        }),
        label='کد ملی',
    )
    birth_day = JalaliDateField(
        widget=AdminJalaliDateWidget(attrs={
            'class': 'jalali_date-date input-ui pr-2',
            'placeholder': 'تاریخ تولد خود را وارد کنید',
        }),
        label='تاریخ تولد'
    )

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if len(national_code) != 10:
            raise forms.ValidationError('کد ملی باید 10 عدد باشد!')
        if re.search(r'^([\s\d]+)$', national_code) is None:
            raise forms.ValidationError('کد ملی باید عدد باشد!')
        return national_code

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise forms.ValidationError('تلفن همراه باید 11 عدد باشد!')
        if re.search(r'^([\s\d]+)$', phone) is None:
            raise forms.ValidationError('شماره همراه باید عدد باشد!')
        return phone


class ChangeUserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class VerifyPhoneForm(forms.Form):
    first_char = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'line-number',
            'maxlength': '1',
            'autofocus': '',
        }))
    second_char = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'line-number',
            'maxlength': '1',
        }))
    third_char = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'line-number',
            'maxlength': '1',
        }))
    fourth_char = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'line-number',
            'maxlength': '1',
        }))
    fifth_char = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'line-number',
            'maxlength': '1',
        }))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VerifyPhoneForm, self).__init__(*args, **kwargs)

    def clean_fifth_char(self):
        first_char = self.cleaned_data.get('first_char')
        second_char = self.cleaned_data.get('second_char')
        third_char = self.cleaned_data.get('third_char')
        fourth_char = self.cleaned_data.get('fourth_char')
        fifth_char = self.cleaned_data.get('fifth_char')
        user = UserProfile.objects.get(user_id=self.request.user.id)
        entered_otp = ''.join([
            str(first_char),
            str(second_char),
            str(third_char),
            str(fourth_char),
            str(fifth_char)
        ])
        if not user.otp:
            raise forms.ValidationError('کد فعالی برای شما وجود ندارد. لطفا درخواست یک کد جدید بدهید.')
        if user.otp_generated_date:
            otp_timeout = datetime.now(timezone.utc) - user.otp_generated_date
            if otp_timeout.days != 0 or otp_timeout.seconds > 120:
                raise forms.ValidationError('کد شما منقضی شده است. لطفا درخواست یک کد جدید بدهید.')
        return entered_otp


class UserAddressForm(forms.Form):
    captcha = ReCaptchaField()
    fullname = forms.CharField(max_length=40,
                               widget=forms.TextInput(attrs={
                                   'class': 'input-ui pr-2 text-right',
                                   'placeholder': 'نام دریافت کننده را وارد نمایید',
                               }),
                               label='نام و نام خانوادگی',
                               )
    phone = forms.CharField(min_length=11, max_length=11,
                            widget=forms.TextInput(attrs={
                                'class': 'input-ui pl-2 dir-ltr text-left',
                                'placeholder': '09xxxxxxxxx',
                            }),
                            label='شماره موبایل',
                            )
    state = forms.ModelChoiceField(queryset=State.objects.all(),
                                   widget=forms.Select(attrs={
                                       'class': 'form-control user-get-cities',
                                       'data-url': '/account/user-get-cities-of-state',
                                   }),
                                   label='استان'
                                   )
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select(attrs={
                                      'class': 'form-control',
                                  }),
                                  label='شهر'
                                  )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-ui pr-2 text-right',
            'placeholder': ' آدرس تحویل گیرنده را وارد نمایید',
        }),
        label='آدرس پستی',
    )
    postal_code = forms.CharField(min_length=10, max_length=10,
                                  widget=forms.TextInput(attrs={
                                      'class': 'input-ui pl-2 dir-ltr text-left placeholder-right',
                                      'placeholder': ' کد پستی را بدون خط تیره بنویسید',
                                  }),
                                  label='کد پستی',
                                  )
    plaque = forms.CharField(max_length=10,
                             widget=forms.TextInput(attrs={
                                 'class': 'input-ui pl-2 dir-ltr text-left placeholder-right',
                                 'placeholder': ' شماره پلاک خود را بنویسید',
                             }),
                             label='پلاک',
                             )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserAddressForm, self).__init__(*args, **kwargs)

    def clean(self):
        user_id = self.request.user.id
        user_addresses = UserAddress.objects.filter(user_id=user_id)
        if user_addresses:
            if user_addresses.count() >= 3:
                messages.error(self.request, 'تعداد مجاز ثبت آدرس برای هر کاربر 3 آدرس می باشد.')
                raise forms.ValidationError('')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if re.search(r'^([\s\d]+)$', phone) is None:
            raise forms.ValidationError('شماره همراه باید عدد باشد.')
        return phone

    def clean_postal_code(self):
        postal_code = self.cleaned_data.get('postal_code')
        if re.search(r'^([\s\d]+)$', postal_code) is None:
            raise forms.ValidationError('کد پستی باید عدد باشد.')
        return postal_code

    def clean_plaque(self):
        plaque = self.cleaned_data.get('plaque')
        if re.search(r'^([\s\d]+)$', plaque) is None:
            raise forms.ValidationError('شماره پلاک باید عدد باشد.')
        return plaque

    def clean_city(self):
        state = self.cleaned_data.get('state')
        city = self.cleaned_data.get('city')
        state_of_city: City = City.objects.filter(city=city).first().state
        if state_of_city != state:
            raise forms.ValidationError('این شهر متعلق به این استان نمی باشد.')
        return city


class UserTicketForm(forms.Form):
    captcha = ReCaptchaField()
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
            'placeholder': 'عنوان تیکت را وارد کنید',
        }),
        label='عنوان',
    )
    question = RichTextUploadingFormField(widget=CKEditorUploadingWidget(), label='متن پرسش')


class UserTicketAnswerForm(forms.Form):
    captcha = ReCaptchaField()
    answer = RichTextUploadingFormField(widget=CKEditorUploadingWidget(), label='متن پاسخ')
