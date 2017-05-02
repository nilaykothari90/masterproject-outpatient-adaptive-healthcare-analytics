from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class UserInformation(models.Model):
	weight = models.FloatField()
	height = models.FloatField()
	dateofbirth = models.IntegerField()
	gender = models.CharField(max_length=1000)
	userid = models.CharField(max_length=1000)
	WeightUnit = models.IntegerField()
	HeightUnit = models.IntegerField()
	nickname = models.CharField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class BPInformation(models.Model):
	NextPageUrl = models.CharField(max_length=1000)
	CurrentRecordCount = models.IntegerField()
	RecordCount = models.IntegerField()
	BPUnit = models.IntegerField()
	PageLength = models.IntegerField()
	PrevPageUrl = models.CharField(max_length=1000)
	PageNumber = models.IntegerField()
	user = models.ForeignKey(UserInformation)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class BPDataList(models.Model):
	DataID = models.CharField(max_length=1000)
	MDate = models.IntegerField()
	LastChangeTime = models.IntegerField()
	HR = models.IntegerField()
	HP = models.IntegerField()
	Lon = models.IntegerField()
	BPL = models.IntegerField()
	time_zone = models.CharField(max_length=1000)
	Note = models.CharField(max_length=1000)
	measurement_time = models.DateTimeField(max_length=1000)
	DataSource = models.CharField(max_length=1000)
	LP = models.IntegerField()
	Lat = models.IntegerField()
	TimeZone = models.CharField(max_length=1000)
	IsArr = models.IntegerField()
	bpInformation = models.ForeignKey(BPInformation)
	user = models.ForeignKey(UserInformation, default="1")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class HRDataInformation(models.Model):
	date = models.DateField()
	value = models.PositiveIntegerField()
	time = models.CharField(max_length=30)
	user = models.ForeignKey(UserInformation)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class DailyActivityInformation(models.Model):
	date = models.CharField(default="1111/11/11", max_length=30)
	steps = models.PositiveIntegerField(unique=True)
	calories = models.PositiveIntegerField()
	distance = models.FloatField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class CurrentHRInformation(models.Model):
	heart_rate = models.PositiveIntegerField()
	date_time = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)



