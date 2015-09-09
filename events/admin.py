from django.contrib import admin

from .models import Event, Edition
from members.models import Member


class ParticipantInline(admin.TabularInline):
    model = Edition.participants.through


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('name', 'description')


class EditionAdmin(admin.ModelAdmin):
    fields = ['date', 'place', 'gallery', 'event', 'max_players']
    list_display = ('event', 'date', 'place')

    inlines = [
        ParticipantInline,
    ]

admin.site.register(Event, EventAdmin)
admin.site.register(Edition, EditionAdmin)
