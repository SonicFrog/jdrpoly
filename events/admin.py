from django.contrib import admin

from .models import Event, Edition


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('name', 'description')


class EditionAdmin(admin.ModelAdmin):
    fields = ['date', 'place', 'gallery', 'event', 'max_players']
    list_display = ('event', 'date', 'place')

admin.site.register(Event, EventAdmin)
admin.site.register(Edition, EditionAdmin)
