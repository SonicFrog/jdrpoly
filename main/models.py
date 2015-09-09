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

    def __str__(self):
        return "%s par %s" % (self.title, self.author)

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Section page d'acceuil")
        verbose_name_plural = _("Sections page d'accueil")
        ordering = ('order', '-pk')


class ComityMember(models.Model):
    """
    Modèle pour un membre du comité
    """
    first_name = models.CharField(max_length=100, verbose_name=_("Prénom"))
    last_name = models.CharField(max_length=100, verbose_name=_("Nom"))
    post = models.CharField(max_length=100, verbose_name=_("Poste"))
    description = models.TextField(verbose_name=_("Description du poste"))
    email = models.EmailField(verbose_name=_("Addresse de contact"))

    def __str__(self):
        return "%s %s, %s pour JDRpoly" % (self.first_name, self.last_name,
                                           self.post)

    class Meta:
        verbose_name = _("Membre du comité")
        verbose_name_plural = _("Membres du comité")
        ordering = ('pk',)
