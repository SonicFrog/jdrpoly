# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _


class Player(models.Model):
    sciper = models.IntegerField(default=0, primary_key=True,
                                 verbose_name=_("SCIPER"))
    name = models.TextField(max_length=200, verbose_name=_("Nom"))
    contaminations = models.IntegerField(default=0,
                                         verbose_name=_("Contaminations"))
    token_spent = models.IntegerField(default=0,
                                      verbose_name=_("Token dépensés"))
    zombie = models.BooleanField(default=False, verbose_name=_("Zombie ?"))
    email = models.EmailField(max_length=300, null=True, verbose_name=_("Email"))

    @classmethod
    def generate_sciper():
        exists = Player.objects().filter(sciper__lt=10000).count() < 0
        new = None
        if exists:
            greatest = Player.objects().filter(sciper__lt=10000)[0]
            new = greatest + 1
        else:
            new = 0
        return new

    @classmethod
    def create(name, sciper=None):
        if sciper is None:
            sciper = Player.generate_sciper()
        player = Player(sciper=sciper)
        player.save()

    @classmethod
    def mail(title, content, zombies):
        mails = Player.objects.filter(zombies=zombies)
        mails = mails.exclude(email__isnull=True)
        mails = [user.email for user in mails]

        message = EmailMessage(subject=title, body=content, bcc=mails)
        message.send()

    def has_contaminated(self, other):
        if self.zombie:
            if not other.contaminate():
                return False
            self.contamination += 1
            self.save()
        return self.zombie

    def add_contamination(self, count):
        if self.zombie:
            self.contamination += count
            self.save()
        return self.zombie

    def contaminate(self):
        if not self.zombie:
            self.zombie = True
            self.save()
        return not self.zombie

    def revive(self):
        if self.zombie:
            self.zombie = False
            self.revive_count += 1
            self.save()
        return self.zombie

    def spend_token(self, count):
        self.token_spent += count
        self.save()
        return self.token_spent

    class Meta:
        verbose_name = _("Joueur")
        verbose_name_plural = _("Joueurs")
        ordering = ('contaminations',)
