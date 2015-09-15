# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0031_auto_20150909_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='member_only',
            field=models.BooleanField(verbose_name='Membres seulement', default=False),
        ),
    ]
