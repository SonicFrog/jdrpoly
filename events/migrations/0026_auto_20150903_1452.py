# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_auto_20150903_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='gallery',
            field=models.ForeignKey(blank=True, to='pictures.Gallery', verbose_name='Gallerie photo', null=True),
        ),
    ]
