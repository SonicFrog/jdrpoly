# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='content',
            field=models.TextField(max_length=30, unique=True),
        ),
    ]
