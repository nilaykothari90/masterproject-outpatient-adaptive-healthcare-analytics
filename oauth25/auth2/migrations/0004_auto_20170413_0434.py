# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-13 04:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0003_auto_20170413_0429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bpdatalist',
            name='user',
        ),
        migrations.DeleteModel(
            name='BPInformation',
        ),
        migrations.DeleteModel(
            name='BPDataList',
        ),
        migrations.DeleteModel(
            name='UserInformation',
        ),
    ]
