# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20150903_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='max_players',
            field=models.IntegerField(null=True, blank=True, verbose_name='Nombre maximum de joueurs'),
        ),
    ]
