# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150817_2213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('date',), 'verbose_name_plural': 'News', 'verbose_name': 'News'},
        ),
    ]
