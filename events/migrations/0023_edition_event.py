# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20150903_0058'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='event',
            field=models.ForeignKey(default=0, verbose_name='Evenement', to='events.Event'),
            preserve_default=False,
        ),
    ]
