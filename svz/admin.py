from django.contrib import admin

from svz.models import Player


class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = (
        'name', 'sciper', 'email', 'contaminations',
        'token_spent', 'zombie',
    )

admin.site.register(Player, PlayerAdmin)
