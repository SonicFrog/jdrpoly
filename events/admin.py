from django.contrib import admin

from .models import Event, Edition


class ParticipantInline(admin.TabularInline):
    model = Edition.participants.through


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_only')


class EditionAdmin(admin.ModelAdmin):
    fields = ['date', 'place', 'gallery', 'event', 'max_players']
    list_display = ('event', 'date', 'place')

    inlines = [
        ParticipantInline,
    ]

admin.site.register(Event, EventAdmin)
admin.site.register(Edition, EditionAdmin)
