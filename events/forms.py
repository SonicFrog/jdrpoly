# coding: utf-8

from django.forms import Form, ModelForm, CharField, Textarea, TextInput
from django.utils.translation import ugettext_lazy as _

from .models import Campaign


class EventPropositionForm(Form):
    name = CharField(max_length=100, label=False,
                     widget=TextInput(attrs={'placeholder':
                                             _('Nom de l\'évenement')}))
    description = CharField(widget=Textarea(attrs={'placeholder':
                                                   _('Description')}),
                            label=False,)

    def __init__(self, user, *args, **kwargs):
        super(EventPropositionForm, self).__init__(*args, **kwargs)
        self.user = user

    def is_valid(self):
        if not super(EventPropositionForm, self).is_valid():
            return False
        if not self.user.profile.is_member():
            self._errors = ['Vous ne pouvez pas proposer de soirées membres sans être membre']
            return False
        return True


class CampaignCreateForm(ModelForm):
    name = CharField(widget=TextInput)

    def is_valid(self):
        if not super(CampaignCreateForm, self).is_valid():
            return False
        out = True
        if not self.cleaned_data['max_players'] > 0:
            self._errors["max_players"] = (
                'Votre campagne doit avoir un nombre positif de joueurs !'
            )
            out = False
        return out

    class Meta:
        model = Campaign
        fields = ['name', 'description', 'max_players', 'start', ]
