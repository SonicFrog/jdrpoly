from django.contrib import admin
from .models import Code, Member


class CodeAdmin(admin.ModelAdmin):
    model = Code
    list_display = ('semesters', 'content')


class MemberAdmin(admin.ModelAdmin):
    model = Member
    list_display = ('location',)
    search_fields = ["user__username"]

admin.site.register(Member, MemberAdmin)
admin.site.register(Code, CodeAdmin)
