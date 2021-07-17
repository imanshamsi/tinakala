from django import forms


class NewslettersForm(forms.Form):
    ip = forms.CharField(max_length=15, required=False, widget=forms.HiddenInput, label='ip')
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'آدرس ایمیل خود را وارد کنید...',
        }),
        label='email')
