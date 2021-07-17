from django import forms
from django.shortcuts import get_object_or_404

from shop_accounts.models import UserAddress


class OrderUserAddress(forms.Form):
    user_address = forms.ModelChoiceField(queryset=UserAddress.objects.none(),
                                          widget=forms.Select(attrs={
                                              'class': 'form-control',
                                          }),
                                          label='آدرس ارسالی')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderUserAddress, self).__init__(*args, **kwargs)
        self.fields['user_address'].queryset = UserAddress.objects.filter(user=self.request.user, is_active=True)

    def clean_user_address(self):
        user_address = self.cleaned_data.get('user_address')
        address = get_object_or_404(UserAddress, address=user_address.address)
        if address.user != self.request.user:
            raise forms.ValidationError('این آدرس متعلق به کاربر جاری نیست!')
        return address
