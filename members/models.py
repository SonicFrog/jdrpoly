# coding: utf-8

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def user_is_staff(user):
    return user.is_staff


def user_is_authenticated(user):
    return user.is_authenticated


def user_is_member(user):
    return user.profile.until > timezone.now()


class Member(models.Model):
    """
    Extended user model with subscription informations added
    """
    user = models.OneToOneField(User, related_name="profile",
                                verbose_name=_("Utilisateur"),
                                parent_link=True)

    until = models.DateField(default=timezone.now,
                             verbose_name=_("Membre jusqu'à"))

    image = models.ImageField(default=None, null=True, blank=True,
                              verbose_name=_("Avatar"))
    location = models.CharField(default=None, null=True, blank=True,
                                max_length=200, verbose_name=_("Localisation"))

    wants_newsletter = models.BooleanField(default=True,
                                           verbose_name=_("Newsletter"))

    def get_absolute_url(self):
        return reverse('other-user-profile', kwargs={'pk': self.pk})

    def is_member(self):
        return self.until > timezone.now()

    def __str__(self):
        return _("Profil utilisateur de %s") % self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_for_new_user(sender, created, instance, **kwargs):
    if created:
        member = Member(user=instance, image=None, location=None,
                        until=timezone.now())
        member.save()


class Code(models.Model):
    """
    One-time use code for validating membership on the website
    """

    CHOICES = ((2, 'Annuelle'),
               (1, 'Semestrielle'))

    content = models.CharField(max_length=30, unique=True,
                               verbose_name=_("Code"))
    semesters = models.IntegerField(choices=CHOICES,
                                    verbose_name=_("Durée"))

    def __str__(self):
        return _("Code valide pour %s semestre(s)") % self.semesters

    class Meta:
        verbose_name = _("Code")
        verbose_name_plural = _("Codes")
        ordering = ("pk",)
