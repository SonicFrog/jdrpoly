# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20150825_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.DurationField(default=None, verbose_name='Durée'),
        ),
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date et heure'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='gallery',
            field=models.ForeignKey(related_name='event', default=None, to='pictures.Gallery', verbose_name='Gallerie photo'),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_players',
            field=models.IntegerField(verbose_name='Nombre max de joueurs'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, default='Nouvel événement', verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Organisateur'),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200, verbose_name='Lieu'),
        ),
    ]
