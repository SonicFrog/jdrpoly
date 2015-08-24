# coding: utf-8

from django import forms


class EventCreationForm(forms.Form):
    image = forms.FileField(required=False, widget=forms.FileInput)
    date = forms.DateTimeField()
    description = forms.Textarea()
    place = forms.TextInput()


class EventParticipationForm(forms.Form):
    pass
