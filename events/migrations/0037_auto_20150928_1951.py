# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0036_auto_20150922_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='start',
            field=models.ForeignKey(verbose_name='Evénement', related_name='animations', to='events.Edition'),
        ),
    ]
