# coding: iso-8859-1

from __future__ import unicode_literals

from django.conf import settings

from django.db import models
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Player(models.Model):
    sciper = models.IntegerField(default=0, primary_key=True,
                                 verbose_name=_("SCIPER"))
    name = models.TextField(max_length=200, verbose_name=_("Nom"))
    contaminations = models.IntegerField(default=0,
                                         verbose_name=_("Contaminations"))
    token_spent = models.IntegerField(default=0,
                                      verbose_name=_("Token dÃ©pensÃ©s"))
    faction = models.BooleanField(default=False, verbose_name=_("Troisième faction?"))
    zombie = models.BooleanField(default=False, verbose_name=_("Zombie ?"))
    email = models.EmailField(max_length=300, null=True, verbose_name=_("Email"))
    classe = models.CharField(max_length=100, null=True, verbose_name=_("Classe"))
    weapon = models.CharField(max_length=100, null=True, verbose_name=_("Arme"))

    @classmethod
    def mail(cls, title, content, zombies):
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
        ordering = ('contaminations', 'token_spent', )


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
    number = models.IntegerField(default=0, verbose_name=_("NumÃ©ro"))
    pdf = models.FileField(upload_to="svz/gazette/%Y", verbose_name=_("PDF"))
    preview = models.ImageField(upload_to="svz/gazette/p/%Y",
                                verbose_name=_("AperÃ§u"))
    short_description = models.TextField(verbose_name=_("Description courte"))

    class Meta:
        ordering = ('-number', )
        verbose_name = _("Gazette")
        verbose_name_plural = _("Gazettes")


class Reward(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    sponsor = models.ForeignKey(Sponsor, verbose_name=_("Sponsor"))

    def __str__(self):
        return "%s offert par %s" % (self.name, self.sponsor)

    class Meta:
        ordering = ('sponsor', 'name')
        verbose_name = _("Lot")
        verbose_name_plural = _("Lots")


class SvZ(models.Model):
    description = models.TextField(max_length=2000, verbose_name=_("Description"))
    start = models.DateField(default=timezone.now, verbose_name=_("Date de début"))
    end = models.DateField(default=timezone.now, verbose_name=_("Date de fin"))
    hour_start = models.IntegerField(default=10, verbose_name=_("Heure de début"))
    hour_end = models.IntegerField(default=19, verbose_name=_("Heure de fin"))
    inscription = models.TextField(default="Entrez les détails", max_length=5000)
    events = models.TextField(default="Entrez un descriptif des évènements", max_length=500)
    place = models.TextField(default="Entrez le lieu", max_length=200)
    rules_vid = models.CharField(default="Entrez l'url youtube de la vidéo des règles",
                                 verbose_name=_("Vidéo de règles Youtube"), max_length=50)
    pres_vid = models.CharField(default="Entrez l'url youtube de la vidéo de présentation",
                                verbose_name=_("Vidéo de présentation Youtube"), max_length=50)

    class Meta:
        verbose_name = _("Détails SvZ")
        verbose_name_plural = _("Détails SvZ")


class Rule(models.Model):
    IMPORTANCE_CHOICES = (
        (0, 'ExtrÃªme'),
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
        ('fa-trophy', 'TrophÃ©'),
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
        verbose_name = _("RÃ¨gle")
        verbose_name_plural = _("RÃ¨gles")
