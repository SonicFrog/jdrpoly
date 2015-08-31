# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20150831_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date et heure', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name='Description', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_players',
            field=models.IntegerField(verbose_name='Nombre max de joueurs', null=True),
        ),
    ]
