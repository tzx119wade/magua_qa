# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-15 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0010_auto_20170515_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='avatar_image', verbose_name='图标'),
        ),
    ]