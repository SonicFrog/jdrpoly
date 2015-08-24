# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_auto_20150815_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpicture',
            name='description',
            field=models.CharField(max_length=200, default='Photo'),
        ),
    ]
