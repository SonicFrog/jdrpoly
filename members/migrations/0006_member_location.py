# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_member_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='location',
            field=models.TextField(max_length=200, default=None),
        ),
    ]
