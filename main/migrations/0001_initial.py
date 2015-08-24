# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_member_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.TextField(max_length=200, default='Nouvelle news')),
                ('content', models.TextField(max_length=10000)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(to='members.Member')),
            ],
        ),
    ]
