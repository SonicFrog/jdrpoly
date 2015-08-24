# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20150722_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpictures',
            name='filename',
            field=models.ImageField(upload_to='', default='Nouvelle photo'),
        ),
    ]
