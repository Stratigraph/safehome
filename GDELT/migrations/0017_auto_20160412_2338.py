# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 23:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GDELT', '0016_eventcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventcode',
            old_name='code',
            new_name='cameoeventcode',
        ),
        migrations.RenameField(
            model_name='eventcode',
            old_name='label',
            new_name='eventdescription',
        ),
    ]
