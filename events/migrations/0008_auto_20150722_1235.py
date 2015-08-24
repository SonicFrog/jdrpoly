# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventpictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpictures',
            name='filename',
            field=models.TextField(default='Nouvelle photo', unique=True),
        ),
    ]
