# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0018_auto_20170426_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyactivityinformation',
            name='date',
            field=models.CharField(default='1111/11/11', max_length=30),
        ),
    ]