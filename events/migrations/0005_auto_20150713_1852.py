# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20150702_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=100, default=datetime.datetime(2015, 7, 13, 18, 52, 38, 503076, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventparticipation',
            name='participates',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200),
        ),
    ]
