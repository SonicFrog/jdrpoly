# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_auto_20150903_1644'),
        ('events', '0028_auto_20150903_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='participants',
            field=models.ManyToManyField(to='members.Member'),
        ),
    ]
