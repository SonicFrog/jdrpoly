# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_remove_member_is_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='image',
        ),
    ]
