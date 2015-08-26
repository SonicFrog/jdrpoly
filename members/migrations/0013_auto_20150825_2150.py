# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0012_auto_20150823_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(parent_link=True, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur'),
        ),
    ]
