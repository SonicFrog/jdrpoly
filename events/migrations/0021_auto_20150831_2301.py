# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0020_auto_20150831_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(verbose_name='Date et heure', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name='Description', default='Evenement'),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_players',
            field=models.IntegerField(verbose_name='Nombre max de joueurs', default=0),
        ),
    ]
