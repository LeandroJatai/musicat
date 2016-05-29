# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-29 05:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160529_0143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='musicahistory',
            options={'ordering': ['-created'], 'verbose_name': 'Música', 'verbose_name_plural': 'Músicas'},
        ),
        migrations.AddField(
            model_name='musica',
            name='titulo',
            field=models.CharField(default='', max_length=256, verbose_name='Título'),
            preserve_default=False,
        ),
    ]
