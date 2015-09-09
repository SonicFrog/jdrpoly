# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_auto_20150903_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='wants_newsletter',
            field=models.BooleanField(default=True, verbose_name='Newsletter'),
        ),
    ]
