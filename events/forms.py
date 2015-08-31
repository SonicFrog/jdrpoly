# coding: utf-8

from django import forms

from .models import Event


class EventCreationForm(forms.ModelForm):
    model = Event

    class Meta:
        fields = ['name', 'place', 'datetime', 'description', 'max_players']



class EventParticipationForm(forms.Form):
    pass
