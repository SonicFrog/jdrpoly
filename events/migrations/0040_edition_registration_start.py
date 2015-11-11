# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0039_auto_20150928_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='edition',
            name='registration_start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='D\xe9but des inscriptions'),
            preserve_default=False,
        ),
    ]
