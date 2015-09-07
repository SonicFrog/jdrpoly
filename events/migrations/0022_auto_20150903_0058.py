# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0002_auto_20150831_1452'),
        ('events', '0021_auto_20150831_2301'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, verbose_name='Date et heure')),
                ('max_players', models.IntegerField(blank=True, verbose_name='Nombre maximum de joueurs')),
                ('place', models.CharField(max_length=100, blank=True, verbose_name='Lieu')),
                ('gallery', models.ForeignKey(to='pictures.Gallery', verbose_name='Gallerie photo')),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='datetime',
        ),
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='event',
            name='gallery',
        ),
        migrations.RemoveField(
            model_name='event',
            name='max_players',
        ),
        migrations.RemoveField(
            model_name='event',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='event',
            name='place',
        ),
    ]
