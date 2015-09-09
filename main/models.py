# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class News(models.Model):
    """
    Modèle pour les articles de news publiés sur la page principale
    """
    author = models.ForeignKey(User, verbose_name=_("Auteur"))
    title = models.CharField(max_length=200, default='Nouvelle news',
                             verbose_name=_("Titre"))
    content = models.TextField(max_length=10000, verbose_name=_("Contenu"))
    date = models.DateField(default=timezone.now, verbose_name=_("Date"))

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ('date',)


class MainPageSection(models.Model):
    """
    Modèle pour une section sur la page d'accueil
    """
    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    content = models.TextField(verbose_name=_("Contenu"))
    order = models.IntegerField(verbose_name=_("Position"))

    class Meta:
        verbose_name = _("Section page d'acceuil")
        verbose_name_plural = _("Sections page d'accueil")
        ordering = ('order', 'pk')
