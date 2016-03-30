# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-30 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svz', '0004_gazette_sponsor'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='url',
            field=models.URLField(default='http://something.ch', verbose_name='Lien externe'),
            preserve_default=False,
        ),
    ]
