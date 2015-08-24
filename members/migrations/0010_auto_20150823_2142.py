# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_auto_20150819_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ('user',), 'verbose_name_plural': 'Profiles', 'verbose_name': 'Profile'},
        ),
        migrations.AlterField(
            model_name='code',
            name='content',
            field=models.CharField(max_length=30, verbose_name='code', unique=True),
        ),
    ]
