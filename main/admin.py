from django.contrib import admin
from .models import CategoryTransition, PaymentType,Transaction,CategoryThings
from datetime import datetime
# Register your models here.


class CategoryTransitionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20

admin.site.register(CategoryTransition,CategoryTransitionAdmin)


class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance', 'image')
    search_fields = ('name',)
    list_filter = ('created_at',)
    save_on_top = True
    list_per_page = 20
    readonly_fields = ('created_at',)
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_at = datetime.now()
        obj.save()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

admin.site.register(PaymentType, PaymentTypeAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category_transition', 'payment_type', 'date', 'amount', 'description', 'created_at')
    search_fields = ('user__name', 'category_transition__name', 'payment_type__name', 'date', 'amount', 'description')
    list_filter = ('created_at',)
    list_editable = ('amount', 'description')
    date_hierarchy = 'date'
    ordering = ('-created_at',)
    autocomplete_fields = [ 'category_transition', 'payment_type']
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.user = request.user
        obj.save()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
    
    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or obj.user == request.user
        else:
            return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or obj.user == request.user
        else:
            return request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_superuser

admin.site.register(Transaction, TransactionAdmin)


class CategoryThingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)
    list_per_page = 20
    list_editable = ('image',)
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_at = datetime.now()
        obj.save()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)
    
    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or obj.user == request.user
        else:
            return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or obj.user == request.user
        else:
            return request.user.is_superuser

admin.site.register(CategoryThings, CategoryThingsAdmin)