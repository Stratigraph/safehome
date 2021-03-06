# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-13 15:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GDELT', '0022_auto_20160413_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='EventBaseCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EventBaseCode', to='GDELT.EventCode'),
        ),
        migrations.AlterField(
            model_name='event',
            name='EventCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EventCode', to='GDELT.EventCode'),
        ),
        migrations.AlterField(
            model_name='event',
            name='EventRootCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='EventRootCode', to='GDELT.EventCode'),
        ),
    ]
