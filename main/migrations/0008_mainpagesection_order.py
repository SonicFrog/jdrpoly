# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150909_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpagesection',
            name='order',
            field=models.IntegerField(unique=True, default=1, verbose_name='Position'),
            preserve_default=False,
        ),
    ]
