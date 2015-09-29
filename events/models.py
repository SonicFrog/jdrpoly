# coding: utf-8

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils import timezone
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
    member_only = models.BooleanField(default=False,
                                      verbose_name=_("Membres seulement"))

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

    participants = models.ManyToManyField(User, related_name='events',
                                          verbose_name=_("Participants"))

    def __str__(self):
        return "%s du %s" % (self.event.name, self.date.__format__("%d/%m/%y"))

    def get_absolute_url(self):
        return reverse('edition-detail', kwargs={'pk': self.pk})

    def register_user(self, user):
        if self.event.member_only:
            allowed = user.profile.is_member()
            if not allowed:
                return False
        self.participants.add(user)
        self.save()
        return True

    def unregister_user(self, user):
        self.participants.remove(user)
        self.save()

    class Meta:
        verbose_name = _("Edition")
        verbose_name_plural = _("Editions")
        ordering = ('-date',)


class Campaign(models.Model):
    """
    Animation pour les soirées membres
    """
    max_players = models.IntegerField(verbose_name=_("Maximum de joueurs"))

    open_for_registration = models.BooleanField(default=True,
                                                verbose_name=_("Accepte les nouveaux joueurs"))

    running = models.BooleanField(default=True, verbose_name=_("En cours"))

    description = models.TextField(verbose_name=_("Description"))
    name = models.CharField(max_length=200, verbose_name=_("Nom"))

    participants = models.ManyToManyField(User, related_name='campaigns',
                                          verbose_name=_("Participants"))
    owner = models.ForeignKey(User, verbose_name=_("Créateur"))

    start = models.ForeignKey(Edition, related_name='animations',
                              verbose_name=_("Evénement"))

    start.queryset = Edition.objects.all().filter(date__gt=timezone.now())

    def __str__(self):
        return "%s à la %s" % (self.name, self.start)

    def register_user(self, user):
        allowed = user.profile.is_member()
        if allowed:
            if (
                    self.participants.count() < self.max_players and
                    self.open_for_registration
            ):
                self.participants.add(user)
                self.save()
            else:
                return False
        return allowed

    def unregister_user(self, user):
        self.participants.remove(user)
        self.save()

    def send_mail_to_participants(self, user, content):
        pass

    def get_absolute_url(self):
        return reverse('campaign-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Campagne")
        verbose_name_plural = _("Campagnes")
        ordering = ('-start',)
