# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_eventpicture_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpicture',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
