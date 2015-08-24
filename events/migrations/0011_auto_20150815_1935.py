# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20150722_1238'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventPictures',
            new_name='EventPicture',
        ),
    ]
