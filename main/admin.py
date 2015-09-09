from django.contrib import admin
from .models import News, MainPageSection, ComityMember


class NewsAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content', 'date']
    list_display = ('title', 'author', 'date')


class SectionAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'order']
    list_display = ('title', 'order', )


class ComityMemberAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'post', 'description', 'email']
    list_display = ('first_name', 'last_name', 'post')


admin.site.register(ComityMember, ComityMemberAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(MainPageSection, SectionAdmin)
