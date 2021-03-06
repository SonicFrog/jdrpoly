from django.contrib import admin

from svz.models import Player, Sponsor, Gazette, Reward, Rule, SvZ


class SvZAdmin(admin.ModelAdmin):
    model = SvZ
    list_display = ('descritiption', 'start')


class PlayerAdmin(admin.ModelAdmin):
    model = Player
    list_display = (
        'name', 'sciper', 'email', 'contaminations',
        'token_spent', 'zombie', 'faction',
    )


class SponsorAdmin(admin.ModelAdmin):
    model = Sponsor
    fields = ('name', 'logo', 'description', 'grade', 'url')
    list_display = (
        'name', 'description', 'grade',
    )


class GazetteAdmin(admin.ModelAdmin):
    model = Gazette
    fields = ('number', 'pdf', 'preview', 'short_description', )
    list_display = ('number', 'short_description')


class RewardAdmin(admin.ModelAdmin):
    model = Reward
    fields = ('name', 'sponsor')
    list_display = ('name', 'sponsor')


class RuleAdmin(admin.ModelAdmin):
    model = Rule
    fields = ('name', 'text', 'icon', 'importance')
    list_display = ('name', 'text', 'importance')

admin.site.register(SvZ)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Gazette, GazetteAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(Rule, RuleAdmin)
