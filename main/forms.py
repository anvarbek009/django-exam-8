from django import forms
from .models import *


class CategoryTransitionForm(forms.ModelForm):
    class Meta:
        model = CategoryTransition
        fields = ['name']

class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = PaymentType
        fields = ['name', 'image']

class CategoryThingsForm(forms.ModelForm):
    class Meta:
        model = CategoryThings
        fields = ['name', 'image']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category_transition', 'payment_type', 'date', 'image', 'amount', 'description']
