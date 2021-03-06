# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-23 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0011_channel_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='标签名')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tag',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='话题标签'),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', to='QA.Tag'),
        ),
    ]
