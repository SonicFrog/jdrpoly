from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'owner', 'description', 'datetime']

    list_display = ('name', 'owner', 'datetime')

admin.site.register(Event, EventAdmin)
