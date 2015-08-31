# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20150825_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(default=None, verbose_name='Avatar', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.CharField(max_length=200, default=None, verbose_name='Localisation', null=True),
        ),
    ]
