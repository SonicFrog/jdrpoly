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
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200, default='Nouvelle news')
    content = models.TextField(max_length=10000)
    date = models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ('date',)
