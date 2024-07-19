from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email','image')
    search_fields = ('name', 'username', 'email','image')
    list_filter = ('created_at',)

admin.site.register(User, UserAdmin)