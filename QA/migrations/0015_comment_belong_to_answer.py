# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-29 08:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0014_comment_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='belong_to_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='QA.Answer'),
        ),
    ]
