# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0035_remove_campaign_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='running',
            field=models.BooleanField(verbose_name='En cours', default=True),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='open_for_registration',
            field=models.BooleanField(verbose_name='Accepte les nouveaux joueurs', default=True),
        ),
    ]
