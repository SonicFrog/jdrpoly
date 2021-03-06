# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Gallery(models.Model):
    """
    Modèle pour une galerie de photos
    """
    name = models.CharField(default=_("Nouvelle galerie"), max_length=50,
                            verbose_name=_("Nom"))
    description = models.TextField(default=None, verbose_name=_("Description"))
    date = models.DateTimeField(default=timezone.now,
                                verbose_name=_("Création"))

    def __unicode__(self):
        return ""

    class Meta:
        verbose_name = _("Galerie")
        verbose_name_plural = _("Galeries")
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('gallery-detail', kwargs={'pk': self.pk})


class Picture(models.Model):
    """
    Image appartenant à une galerie
    """
    image = models.ImageField(default=None, upload_to="svz/pictures/%Y-%m-%d",
                              verbose_name=_("Image"))
    comment = models.CharField(default=None, verbose_name=_("Commentaire"),
                               max_length=100)
    owner = models.ForeignKey(User, related_name='pictures',
                              verbose_name=_("Uploadeur"))
    gallery = models.ForeignKey(Gallery, verbose_name=_("Galerie"),
                                related_name='pictures')
    date = models.DateTimeField(default=timezone.now,
                                verbose_name=_("Mise en ligne"))

    def __unicode__(self):
        return ""

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
        ordering = ('-date',)
