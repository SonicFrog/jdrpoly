# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-09 14:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('svz', '0002_auto_20161213_2212'),
    ]

    operations = [
        migrations.CreateModel(
            name='SvZ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000, verbose_name='Description')),
                ('start', models.DateField(default=django.utils.timezone.now, verbose_name='Date de d\xc3\xa9but')),
                ('end', models.DateField(default=django.utils.timezone.now, verbose_name='Date de fin')),
                ('hour_start', models.IntegerField(default=10, verbose_name='Heure de d\xe9but')),
                ('hour_end', models.IntegerField(default=19, verbose_name='Heure de fin')),
                ('inscription', models.CharField(default='Entrez les d\xc3\xa9tails', max_length=5000)),
                ('events', models.CharField(default='Entrez un descriptif des \xc3\xa9venements', max_length=500)),
                ('place', models.CharField(default='Entrez le lieu', max_length=200)),
                ('rules_vid', models.URLField(default="Entrez l'url youtube de la vid\xc3\xa9o des r\xc3\xa8gles")),
                ('pres_vid', models.URLField(default="Entrez l'url youtube de la vid\xc3\xa9o de pr\xc3\xa9sentation")),
            ],
            options={
                'verbose_name': 'D\xc3\xa9tails SvZ',
            },
        ),
        migrations.AlterModelOptions(
            name='rule',
            options={'ordering': ('importance',), 'verbose_name': 'R\xc3\xa8gle', 'verbose_name_plural': 'R\xc3\xa8gles'},
        ),
        migrations.AlterField(
            model_name='gazette',
            name='number',
            field=models.IntegerField(default=0, verbose_name='Num\xc3\xa9ro'),
        ),
        migrations.AlterField(
            model_name='gazette',
            name='preview',
            field=models.ImageField(upload_to='svz/gazette/p/%Y', verbose_name='Aper\xc3\xa7u'),
        ),
        migrations.AlterField(
            model_name='player',
            name='token_spent',
            field=models.IntegerField(default=0, verbose_name='Token d\xc3\xa9pens\xc3\xa9s'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='icon',
            field=models.CharField(choices=[('fa-lock', 'Cadenas'), ('fa-cog', 'Rouage'), ('fa-user', 'Personne'), ('fa-male', 'Homme'), ('fa-female', 'Femme'), ('fa-server', 'Serveur'), ('fa-crosshair', 'Viseur'), ('fa-check', 'Check'), ('fa-ticket', 'Ticket'), ('fa-heartbeat', 'Coeur'), ('fa-medkit', 'Medkit'), ('fa-trophy', 'Troph\xc3\xa9')], max_length=20, verbose_name='Icone'),
        ),
        migrations.AlterField(
            model_name='rule',
            name='importance',
            field=models.IntegerField(choices=[(0, 'Extr\xc3\xaame'), (1, 'Haute'), (2, 'Moyenne'), (3, 'Faible')], default=1, verbose_name='Importance'),
        ),
    ]
