from django.contrib import admin
from django.contrib.auth.models import User
from .models import Code, Member


class ProfileInline(admin.TabularInline):
    model = Member


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name')
    inlines = [
        ProfileInline
    ]


class CodeAdmin(admin.ModelAdmin):
    model = Code
    list_display = ('semesters', 'content')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Code, CodeAdmin)
