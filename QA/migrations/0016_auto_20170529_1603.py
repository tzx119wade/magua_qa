# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-29 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0015_comment_belong_to_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='QA.Comment'),
        ),
    ]
