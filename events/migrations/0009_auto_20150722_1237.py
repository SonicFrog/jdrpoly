# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20150722_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpictures',
            name='filename',
            field=models.FilePathField(unique=True, default='Nouvelle photo'),
        ),
    ]
