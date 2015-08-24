# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Day',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
        migrations.AddField(
            model_name='event',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 2, 14, 39, 23, 304923, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
