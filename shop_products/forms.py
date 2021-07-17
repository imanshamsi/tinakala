from captcha.fields import ReCaptchaField
from django import forms

from shop_categories.models import SubCategoryParent, Brands
from shop_products.models import ProductComment


class ProductSendCommentsForm(forms.Form):
    ADVISED_CHOICES = (
        (1, 'این محصول را توصیه می کنم'),
        (0, 'این محصول را توصیه نمی کنم'),
    )
    captcha = ReCaptchaField()
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-ui pr-2 text-right',
            'placeholder': 'عنوان نظر را وارد نمایید',
        }),
        label='عنوان نظر'
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'input-ui pr-2 text-right',
            'placeholder': ' متن نظر را وارد نمایید',
        }),
        label='متن نظر'
    )
    advised = forms.IntegerField(
        widget=forms.Select(choices=ADVISED_CHOICES, attrs={
            'class': 'custom-select',
        }),
        label='آیا خرید این محصول را پیشنهاد می کنید؟'
    )
    worth = forms.IntegerField(
        widget=forms.Select(choices=ProductComment.COMMENT_CHOICES, attrs={
            'class': 'custom-select',
        }),
        label='ارزش خرید را چگونه برآورد می کنید؟'
    )
    quality = forms.IntegerField(
        widget=forms.Select(choices=ProductComment.COMMENT_CHOICES, attrs={
            'class': 'custom-select',
        }),
        label='کیفیت ساخت را چگونه برآورد می کنید؟'
    )
    function = forms.IntegerField(
        widget=forms.Select(choices=ProductComment.COMMENT_CHOICES, attrs={
            'class': 'custom-select',
        }),
        label='عملکرد را چگونه برآورد می کنید؟'
    )

    def clean_advised(self):
        advised = self.cleaned_data.get('advised')
        if advised not in [item[0] for item in self.ADVISED_CHOICES]:
            raise forms.ValidationError('مقدار نامعتبر برای این فیلد وارد شده است.')
        return advised

    def clean_worth(self):
        worth = self.cleaned_data.get('worth')
        if worth not in [item[0] for item in ProductComment.COMMENT_CHOICES]:
            raise forms.ValidationError('مقدار نامعتبر برای این فیلد وارد شده است.')
        return worth

    def clean_quality(self):
        quality = self.cleaned_data.get('quality')
        if quality not in [item[0] for item in ProductComment.COMMENT_CHOICES]:
            raise forms.ValidationError('مقدار نامعتبر برای این فیلد وارد شده است.')
        return quality

    def clean_function(self):
        function = self.cleaned_data.get('function')
        if function not in [item[0] for item in ProductComment.COMMENT_CHOICES]:
            raise forms.ValidationError('مقدار نامعتبر برای این فیلد وارد شده است.')
        return function


class ProductByCategoryBrandFilterForm(forms.Form):
    brands = forms.ModelMultipleChoiceField(queryset=SubCategoryParent.objects.none(), required=False,
                                            widget=forms.CheckboxSelectMultiple,
                                            label='برند',)
    price_start = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'input-ui pr-2',
        }),
        label='قیمت از (تومان)',
        required=False,)
    price_end = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'input-ui pr-2',
        }),
        label='قیمت تا (تومان)',
        required=False)
    is_exist = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='فقط کالاهای موجود')

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)
        super(ProductByCategoryBrandFilterForm, self).__init__(*args, **kwargs)
        self.fields['brands'].queryset = Brands.objects.filter(categories=self.category).distinct()
