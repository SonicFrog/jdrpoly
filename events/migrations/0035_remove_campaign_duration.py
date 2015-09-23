# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0034_auto_20150922_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='duration',
        ),
    ]
