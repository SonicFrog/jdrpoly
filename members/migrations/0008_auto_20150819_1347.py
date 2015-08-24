# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_auto_20150818_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='profile_image', default=None),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_member',
            field=models.BooleanField(verbose_name='active_member', default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.CharField(verbose_name='member_location', max_length=200, default=None),
        ),
        migrations.AlterField(
            model_name='member',
            name='until',
            field=models.DateField(verbose_name='active_member_end', default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='member',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user', verbose_name='user'),
        ),
    ]
