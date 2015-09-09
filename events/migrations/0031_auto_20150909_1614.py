# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0030_auto_20150908_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='edition',
            name='participants',
            field=models.ManyToManyField(verbose_name='Participants', to=settings.AUTH_USER_MODEL, related_name='events'),
        ),
    ]
