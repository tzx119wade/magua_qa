# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-11 08:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0003_auto_20170511_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publisher', to='QA.UserProfile', verbose_name='发布人'),
        ),
    ]
