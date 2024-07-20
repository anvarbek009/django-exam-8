from django.contrib import admin
from .models import User
from datetime import datetime
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email','image')
    search_fields = ('name', 'username', 'email','image')
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
            return qs.filter(id=request.user.id)
    

    def has_change_permission(self, request, obj=None):
        if obj:
            return request.user.is_superuser or obj.id == request.user.id
        else:
            return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or obj.id == request.user.id
    
    


admin.site.register(User, UserAdmin)