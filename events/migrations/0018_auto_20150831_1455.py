# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_auto_20150831_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0, 3600), verbose_name='Durée'),
        ),
    ]
