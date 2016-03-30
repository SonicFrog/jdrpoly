from django.contrib import admin

from svz.models import Player, Sponsor


class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = (
        'name', 'sciper', 'email', 'contaminations',
        'token_spent', 'zombie',
    )


class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    fields = ('name', 'logo', 'description', 'grade', 'url')
    list_display = (
        'name', 'description', 'grade',
    )


admin.site.register(Player, PlayerAdmin)
admin.site.register(Sponsor, SponsorAdmin)
