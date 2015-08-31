# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20150831_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.DurationField(verbose_name='Durée'),
        ),
    ]