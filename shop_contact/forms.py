import re

from django import forms


class ContactUsForm(forms.Form):
    fullname = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
        }),
        label='نام و نام خانوادگی',
    )
    phone = forms.CharField(max_length=11, min_length=11,
                            widget=forms.TextInput(attrs={
                                'class': 'input-ui pr-2',
                            }),
                            label='شماره همراه',
                            )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-ui pr-2',
        }),
        label='ایمیل',
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2',
        }),
        label='عنوان پیام',
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-ui pr-2 text-right',
            'placeholder': 'متن پیام را وارد کنید',
        }),
        label='متن پیام',
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if re.search(r'^([\s\d]+)$', phone) is None:
            raise forms.ValidationError('شماره همراه باید عدد باشد!')
        return phone
