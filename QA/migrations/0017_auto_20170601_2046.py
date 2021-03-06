# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-01 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0016_auto_20170529_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replys', to='QA.Comment'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='choose',
            field=models.CharField(blank=True, choices=[('like', 'like'), ('unlike', 'unlike'), ('none', 'none')], max_length=10, null=True),
        ),
    ]
