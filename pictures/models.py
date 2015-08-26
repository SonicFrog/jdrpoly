# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Gallery(models.Model):
    """
    Modèle pour une gallerie de photos
    """
    name = models.CharField(default=_("Nouvelle galerie"), max_length=50,
                            verbose_name=_("Nom"))
    description = models.TextField(default=None, verbose_name=_("Description"))
    date = models.DateTimeField(default=timezone.now,
                                verbose_name=_("Création"))

    class Meta:
        verbose_name = _("Gallerie")
        verbose_name = _("Galleries")
        ordering = ('-date',)


class Picture(models.Model):
    """
    Image appartenant à une gallerie
    """
    image = models.ImageField(default=None, verbose_name=_("Image"))
    comment = models.CharField(default=None, verbose_name=_("Commentaire"),
                               max_length=100)
    owner = models.ForeignKey(User, related_name='pictures',
                              verbose_name=_("Uploadeur"))
    gallery = models.ForeignKey(Gallery, verbose_name=_("Gallerie"),
                                related_name='pictures')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")
        ordering = ('-date',)