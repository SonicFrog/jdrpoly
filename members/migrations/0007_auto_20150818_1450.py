# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_member_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
