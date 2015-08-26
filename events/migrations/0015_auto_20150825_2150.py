# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pictures', '0001_initial'),
        ('events', '0014_auto_20150823_2154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpicture',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='gallery',
            field=models.ForeignKey(related_name='event', default=None, to='pictures.Gallery'),
        ),
        migrations.DeleteModel(
            name='EventPicture',
        ),
    ]
