# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth2', '0022_hrdatainformation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hrdatainformation',
            name='date',
            field=models.DateField(),
        ),
    ]