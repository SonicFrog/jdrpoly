# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from pictures.models import Gallery


class Event(models.Model):
    """
    Type d'évenement
    """
    name = models.CharField(max_length=100, default=_('Nouvel événement'),
                            verbose_name=_("Nom"))
    description = models.TextField(default=_("Evenement"),
                                   verbose_name=_("Description"))

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Evenement")
        verbose_name_plural = _("Evenements")
        ordering = ('name',)


class Edition(models.Model):
    """
    Edition d'un évenement
    """
    date = models.DateTimeField(verbose_name=_("Date et heure"), blank=True)
    max_players = models.IntegerField(blank=True, null=True,
                                      verbose_name=_("Nombre maximum de joueurs"),)

    place = models.CharField(max_length=100, verbose_name=_("Lieu"),
                             blank=True)
    gallery = models.ForeignKey(Gallery, verbose_name=_("Gallerie photo"),
                                blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name=_("Evenement"),
                              related_name='editions')

    participants = models.ManyToManyField(User, related_name='events')

    def __str__(self):
        return "%s du %s" % (self.event.name, self.date)

    def get_absolute_url(self):
        return reverse('edition-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Edition")
        verbose_name_plural = _("Editions")
        ordering = ('-date',)
