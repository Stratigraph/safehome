# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDELT', '0028_auto_20160413_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gdeltfile',
            name='filename',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.AlterField(
            model_name='gdeltfile',
            name='md5',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]