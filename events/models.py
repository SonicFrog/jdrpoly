# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from pictures.models import Gallery


class Event(models.Model):
    """
    Evenement générique (week-end, murder, soirées libres, ...)
    """
    name = models.CharField(max_length=100, default=_('Nouvel événement'))
    owner = models.ForeignKey(User)
    place = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    max_players = models.IntegerField()
    gallery = models.ForeignKey(Gallery, default=None, related_name='event')

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class EventParticipation(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
