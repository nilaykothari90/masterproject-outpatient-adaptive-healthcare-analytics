# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 03:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0030_auto_20170428_0348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitbitdailyactivityinformation',
            name='calories',
            field=models.PositiveIntegerField(),
        ),
    ]
