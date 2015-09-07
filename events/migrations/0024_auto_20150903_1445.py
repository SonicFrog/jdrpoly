# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0023_edition_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='edition',
            options={'verbose_name_plural': 'Editions', 'verbose_name': 'Edition', 'ordering': ('-date',)},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name_plural': 'Evenements', 'verbose_name': 'Evenement', 'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='edition',
            name='event',
            field=models.ForeignKey(verbose_name='Evenement', to='events.Event', related_name='edition'),
        ),
    ]
