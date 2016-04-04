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

    def __str__(self):
        zombie = "Zombie" if self.zombie else "Humain"
        return "%s %s" % (self.name, zombie)

    class Meta:
        verbose_name = _("Joueur")
        verbose_name_plural = _("Joueurs")
        ordering = ('contaminations',)


class Sponsor(models.Model):
    SPONSOR_GRADES = (
        (1, 'Bronze'),
        (2, 'Silver'),
        (3, 'Gold'),
        (4, 'Platinum'),
    )

    name = models.CharField(max_length=200, default=_("Nouveau sponsor"),
                            verbose_name=_("Nom"))
    description = models.TextField(default=_("Aucune description"),
                                   verbose_name=_("Description"))
    grade = models.IntegerField(choices=SPONSOR_GRADES,
                                verbose_name=_("Grade"))
    logo = models.ImageField(upload_to='svz/sponsors/%Y',
                             height_field="logo_height",
                             width_field="logo_width")
    logo_width = models.IntegerField(default=125, verbose_name=_("Largeur"))
    logo_height = models.IntegerField(default=125, verbose_name=_("Hauteur"))
    url = models.URLField(verbose_name=_("Lien externe"))

    def __str__(self):
        return "%s - sponsor %s" % (self.name, self.get_grade_display())

    class Meta:
        ordering = ('-grade', )
        verbose_name = _("Sponsor")
        verbose_name_plural = _("Sponsors")


class Gazette(models.Model):
    number = models.IntegerField(default=0, verbose_name=_("Numéro"))
    pdf = models.FileField(upload_to="svz/gazette/%Y", verbose_name=_("PDF"))
    preview = models.ImageField(upload_to="svz/gazette/p/%Y",
                                verbose_name=_("Aperçu"))
    short_description = models.TextField(verbose_name=_("Description courte"))

    class Meta:
        ordering = ('number', )
        verbose_name = _("Gazette")
        verbose_name_plural = _("Gazettes")


class Reward(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    sponsor = models.ForeignKey(Sponsor, verbose_name=_("Sponsor"))

    def __str__(self):
        return "%s offert par %s" % (self.name, self.sponsor)

    def meta(self):
        return self._meta

    class Meta:
        ordering = ('sponsor', 'name')
        verbose_name = _("Lot")
        verbose_name_plural = _("Lots")


class Rule(models.Model):
    IMPORTANCE_CHOICES = (
        (0, 'Extrême'),
        (1, "Haute"),
        (2, "Moyenne"),
        (3, "Faible"),
    )

    ICON_CHOICES = (
        ('fa-lock', 'Cadenas'),
        ('fa-cog', 'Rouage'),
        ('fa-user', 'Personne'),
        ('fa-male', 'Homme'),
        ('fa-female', 'Femme'),
        ('fa-server', 'Serveur'),
        ('fa-crosshair', 'Viseur'),
        ('fa-check', 'Check'),
        ('fa-ticket', 'Ticket'),
        ('fa-heartbeat', 'Coeur'),
        ('fa-medkit', 'Medkit'),
        ('fa-trophy', 'Trophé'),
    )
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    text = models.TextField(max_length=500, verbose_name=_("Contenu"))
    icon = models.CharField(max_length=20, verbose_name=_("Icone"),
                            choices=ICON_CHOICES)
    importance = models.IntegerField(choices=IMPORTANCE_CHOICES, default=1,
                                     verbose_name=_("Importance"))

    def __str__(self):
        return "%s - %s" % (self.name, self.get_importance_display())

    class Meta:
        ordering = ('importance', )
        verbose_name = _("Règle")
        verbose_name_plural = _("Règles")
