from django.contrib import admin
# Register your models here.

from .models import User


class PageUser(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'password')
    ordering = ('full_name',)
    search_fields = ('full_name',)


admin.site.register(User, PageUser)
