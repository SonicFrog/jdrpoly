from django.contrib import admin
from .models import News


class NewsAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'content', 'date']
    list_display = ('title', 'author', 'date')

admin.site.register(News, NewsAdmin)
