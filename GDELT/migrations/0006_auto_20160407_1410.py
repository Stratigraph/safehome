# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-07 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDELT', '0005_auto_20160407_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gkgcounts',
            name='cameoeventids',
            field=models.CommaSeparatedIntegerField(max_length=2048),
        ),
    ]
