# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 03:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0025_auto_20170428_0311'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DailyActivityInformation',
        ),
    ]