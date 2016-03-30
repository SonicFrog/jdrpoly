# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-22 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svz', '0002_auto_20160301_1444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('contaminations',), 'verbose_name': 'Joueur', 'verbose_name_plural': 'Joueurs'},
        ),
        migrations.RemoveField(
            model_name='player',
            name='revive_count',
        ),
        migrations.AlterField(
            model_name='player',
            name='contaminations',
            field=models.IntegerField(default=0, verbose_name='Contaminations'),
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(max_length=300, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.TextField(max_length=200, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='player',
            name='sciper',
            field=models.IntegerField(default=0, primary_key=True, serialize=False, verbose_name='SCIPER'),
        ),
        migrations.AlterField(
            model_name='player',
            name='token_spent',
            field=models.IntegerField(default=0, verbose_name='Token d\xe9pens\xe9s'),
        ),
        migrations.AlterField(
            model_name='player',
            name='zombie',
            field=models.BooleanField(default=False, verbose_name='Zombie ?'),
        ),
    ]