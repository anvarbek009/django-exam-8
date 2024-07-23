from django import forms
from .models import *


class CategoryTransitionForm(forms.ModelForm):
    class Meta:
        model = CategoryTransition
        fields = ['name']

class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = ['name', 'image','balance']

class CategoryThingsForm(forms.ModelForm):
    class Meta:
        model = CategoryThings
        fields = ['name', 'image']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category_transition', 'payment_type', 'date', 'image', 'amount', 'description']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['payment_type'].queryset = PaymentType.objects.filter(user=user)
