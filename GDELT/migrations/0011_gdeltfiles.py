# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GDELT', '0010_auto_20160407_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='GDELTFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=256)),
            ],
        ),
    ]
