from django.contrib import admin

from .models import Event, Edition, Campaign


class ParticipantInline(admin.TabularInline):
    model = Edition.participants.through


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_only')
    fieldsets = [
        (None, {'fields': ['name', 'description']}),
        ('Membres', {'fields': ['member_only']}),
    ]


class EditionAdmin(admin.ModelAdmin):
    fields = ['date', 'place', 'gallery', 'event', 'max_players']
    list_display = ('event', 'date', 'place')


class CampaignAdmin(admin.ModelAdmin):
    fields = [
        'name', 'description', 'start', 'owner', 'open_for_registration',
        'max_players'
    ]
    list_display = ('name', 'start', 'owner')


admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Edition, EditionAdmin)
