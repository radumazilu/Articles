# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_remove_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='playlist_creator',
            field=models.CharField(max_length=200),
        ),
    ]