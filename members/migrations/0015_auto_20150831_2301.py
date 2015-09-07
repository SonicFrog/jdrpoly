# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_auto_20150831_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(verbose_name='Avatar', null=True, default=None, blank=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.CharField(blank=True, max_length=200, verbose_name='Localisation', null=True, default=None),
        ),
    ]
