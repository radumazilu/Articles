# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-10 21:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20161210_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='playlist',
            name='is_favourite',
            field=models.BooleanField(default=False),
        ),
    ]
