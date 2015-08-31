# coding: utf-8

from datetime import timedelta

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
    name = models.CharField(max_length=100, default=_('Nouvel événement'),
                            verbose_name=_("Nom"))
    owner = models.ForeignKey(User, verbose_name=_("Organisateur"))
    place = models.CharField(max_length=200, verbose_name=_("Lieu"))
    datetime = models.DateTimeField(default=timezone.now,
                                    verbose_name=_("Date et heure"))
    duration = models.DurationField(verbose_name=_("Durée"))
    description = models.TextField(verbose_name=_("Description"))
    max_players = models.IntegerField(verbose_name=_("Nombre max de joueurs"))
    gallery = models.ForeignKey(Gallery, default=None, related_name='event',
                                verbose_name=_("Gallerie photo"))

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class EventParticipation(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
