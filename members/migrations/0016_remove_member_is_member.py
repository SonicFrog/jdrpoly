# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0015_auto_20150831_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='is_member',
        ),
    ]
