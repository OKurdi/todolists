from django.contrib import admin
# Register your models here.

from .models import User
from .models import TodoList
from .models import Entry


class PageUser(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'password')
    ordering = ('full_name',)
    search_fields = ('full_name',)


admin.site.register(User, PageUser)
admin.site.register(TodoList)
admin.site.register(Entry)

