from django.contrib import admin
from .models import CategoryTransition, PaymentType,Transaction,CategoryThings
from datetime import datetime
# Register your models here.

admin.site.register(CategoryTransition)
admin.site.register(PaymentType)
admin.site.register(Transaction)
admin.site.register(CategoryThings)