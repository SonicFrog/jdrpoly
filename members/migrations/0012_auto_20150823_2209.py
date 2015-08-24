# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20150823_2154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='code',
            options={'verbose_name': 'Code', 'ordering': ('pk',), 'verbose_name_plural': 'Codes'},
        ),
    ]
