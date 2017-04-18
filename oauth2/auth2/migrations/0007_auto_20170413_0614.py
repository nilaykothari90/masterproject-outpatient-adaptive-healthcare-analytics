# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-13 06:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth2', '0006_auto_20170413_0612'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPDataList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DataID', models.CharField(max_length=1000)),
                ('MDate', models.IntegerField()),
                ('LastChangeTime', models.IntegerField()),
                ('HR', models.IntegerField()),
                ('HP', models.IntegerField()),
                ('Lon', models.IntegerField()),
                ('BPL', models.IntegerField()),
                ('time_zone', models.CharField(max_length=1000)),
                ('Note', models.CharField(max_length=1000)),
                ('measurement_time', models.CharField(max_length=1000)),
                ('DataSource', models.CharField(max_length=1000)),
                ('LP', models.IntegerField()),
                ('Lat', models.IntegerField()),
                ('TimeZone', models.CharField(max_length=1000)),
                ('IsArr', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BPInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NextPageUrl', models.CharField(max_length=1000)),
                ('CurrentRecordCount', models.IntegerField()),
                ('RecordCount', models.IntegerField()),
                ('BPUnit', models.IntegerField()),
                ('PageLength', models.IntegerField()),
                ('PrevPageUrl', models.CharField(max_length=1000)),
                ('PageNumber', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('dateofbirth', models.IntegerField()),
                ('gender', models.CharField(max_length=1000)),
                ('userid', models.CharField(max_length=1000)),
                ('WeightUnit', models.IntegerField()),
                ('HeightUnit', models.IntegerField()),
                ('nickname', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='bpinformation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth2.UserInformation'),
        ),
        migrations.AddField(
            model_name='bpdatalist',
            name='bpInformation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth2.BPInformation'),
        ),
    ]
