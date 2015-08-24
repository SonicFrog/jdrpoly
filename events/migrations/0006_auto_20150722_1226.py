# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20150713_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventparticipation',
            name='participates',
        ),
        migrations.AddField(
            model_name='event',
            name='max_players',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default='Nouvel événement', max_length=100),
        ),
    ]
