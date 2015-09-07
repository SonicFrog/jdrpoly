# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_auto_20150903_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='event',
            field=models.ForeignKey(verbose_name='Evenement', related_name='editions', to='events.Event'),
        ),
    ]
