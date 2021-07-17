from django import forms


class AddProductToCart(forms.Form):
    PRODUCT_COUNT_CHOICE = [(i, str(i)) for i in range(1, 6)]
    product_count = forms.TypedChoiceField(required=False, choices=PRODUCT_COUNT_CHOICE, coerce=int,
                                           widget=forms.Select(attrs={
                                               'class': 'form-control'
                                           })
                                           )
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.inventory = kwargs.pop('inventory', None)
        super(AddProductToCart, self).__init__(*args, **kwargs)
        if self.inventory and self.inventory < 5:
            self.fields['product_count'].choices = [(i, str(i)) for i in range(1, self.inventory + 1)]

    def clean_product_count(self):
        product_count = self.cleaned_data.get('product_count')
        print(product_count)
        if product_count:
            if self.inventory < product_count:
                raise forms.ValidationError('درخواست بیشتر از موجودی کالا است!')
            if product_count > 5:
                raise forms.ValidationError('درخواست بیشتر از حد مجاز است!')
        return product_count
