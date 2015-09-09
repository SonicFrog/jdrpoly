from django.contrib import admin
from .models import News, MainPageSection


class NewsAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content', 'date']
    list_display = ('title', 'author', 'date')


class SectionAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'order']
    list_display = ('title', 'order', )


admin.site.register(News, NewsAdmin)
admin.site.register(MainPageSection, SectionAdmin)
