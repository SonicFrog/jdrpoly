# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    """
    Evenement générique (week-end, murder, soirées libres, ...)
    """
    name = models.CharField(max_length=100, default='Nouvel événement')
    owner = models.ForeignKey(User)
    place = models.CharField(max_length=200)
    datetime = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    max_players = models.IntegerField()

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class EventPicture(models.Model):
    """
    Modèle pour une image qui appartient à un évenement (ou pas)
    """
    filename = models.ImageField(default='Nouvelle photo',
                                 verbose_name=_("Image"))
    description = models.CharField(max_length=200, default='Photo',
                                   verbose_name=_("Description"))
    date = models.DateTimeField(default=timezone.now, verbose_name=_("Date"))

    event = models.ForeignKey(Event)

    def get_absolute_url(self):
        return reverse('event-picture', kwargs={'pk': self.pk})


class EventParticipation(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
