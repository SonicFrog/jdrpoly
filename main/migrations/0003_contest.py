# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-13 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nom')),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateField(verbose_name='Date limite')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Concours',
                'verbose_name_plural': 'Concours',
            },
        ),
    ]
