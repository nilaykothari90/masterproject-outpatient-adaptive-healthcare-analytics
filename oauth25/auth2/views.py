from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
import time

from auth2.models import BPInformation, BPDataList, UserInformation, HRDataInformation, DailyActivityInformation, CurrentHRInformation
import auth2.serializers

# Create your views here.

@csrf_exempt
def getData(request):
	# year = 2017
	# month = 04
	# day = 22 
	year = int(request.GET.get('year'))
	month = int(request.GET.get('month'))
	day = int(request.GET.get('day'))
	user_info = UserInformation.objects.filter(userid = "699ccacbe63b4030826c8a32349f2e3e")
	data = {}
	user_dct = {}

	for obj in user_info:
		user_dct['weight'] = obj.weight
		user_dct['height'] = obj.height
		user_dct['dateofbirth'] = obj.dateofbirth
		user_dct['gender'] = obj.gender
		user_dct['WeightUnit'] = obj.WeightUnit
		user_dct['HeightUnit'] = obj.HeightUnit
		user_dct['nickname'] = obj.nickname

	bp_data_lst = []
	bp_data_list = BPDataList.objects.filter(measurement_time__startswith = datetime.date(year, month, day))

	for obj in bp_data_list:
		bp_data_dct = {}
		bp_data_dct['HR'] = obj.HR
		bp_data_dct['HP'] = obj.HP
		bp_data_dct['BPL'] = obj.BPL
		bp_data_dct['measurement_time'] = str(obj.measurement_time)
		bp_data_dct['LP'] = obj.LP
		bp_data_lst.append(bp_data_dct)

	hr_data_list = []
	hr_data_objs = HRDataInformation.objects.filter(date__startswith = datetime.date(year, month, day))

	for obj in hr_data_objs:
		hr_data_dct = {}
		hr_data_dct['date'] = obj.date
		hr_data_dct['value'] = obj.value
		hr_data_dct['time'] = obj.time
		hr_data_list.append(hr_data_dct)


	current_hr_data = {}
	current_hr_objs = CurrentHRInformation.objects.filter(date_time__startswith = datetime.date(year, month, day))
	
	for obj in current_hr_objs:
		current_hr_data['heart_rate'] = obj.heart_rate
		current_hr_data['date_time'] = str(obj.date_time)

	data = {
		"user_info": user_dct,
		"bp_data_list": bp_data_lst,
		"hr_data_list": hr_data_list,
		"current_hr_data": current_hr_data
	}


	print json.dumps(data)
	return HttpResponse(json.dumps(data))


@csrf_exempt
def getIHealthBP(request):

	url = "https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?client_id=685895e7db4d420799808416d8fbb95b&response_type=code&redirect_uri=http://localhost:8000/callback/&APIName=OpenApiBP"
	print_header("Getting Code")
	r = requests.get(url)
	print r
	return HttpResponseRedirect(url)

@csrf_exempt
def callback(request):
	code = request.GET.get('code')
	print "code: " + code

	client_id = "client_id=685895e7db4d420799808416d8fbb95b&"
	client_secret = "client_secret=6b633671d03f4e43a7d9a55e4ddeb9fd&"
	grant_type = "grant_type=authorization_code&"
	redirect_uri = "redirect_uri=http://localhost:8000/callback/&"

	url = "https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?" + client_id + client_secret + grant_type + redirect_uri + "code=" + code

	print_header("Getting Token")
	r = requests.get(url)
	r_json = r.json()
	print r
	# print r_json
	access_token = r_json['AccessToken']
	refresh_token = r_json['RefreshToken']
	response_type = "response_type=refresh_token&"
	user_id = r_json['UserID']

	# To get the new access token based on refresh token
	url = "https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?" + client_id + client_secret + redirect_uri + response_type + "refresh_token=" + refresh_token + "&UserID=" + user_id

	print_header("Getting Access Token")
	r = requests.get(url)
	print r
	r_json = r.json()
	# print r_json
	access_token = r_json['AccessToken']
	
	# To get the User information based on access token
	sc_user_info = "&sc=89ec14345f8948c891ba804a7c3ff68c"
	sv_user_info = "&sv=9823bbc6f2904b0fad40bb32c9dd4b2c"
	print_header("Requesting User Information")
	url = "https://api.ihealthlabs.com:8443/openapiv2/user/" + user_id + ".json/?" + client_id + client_secret + redirect_uri + "access_token=" + access_token + sc_user_info + sv_user_info + "&locale=en_US"
	# print url
	r = requests.get(url)
	print r
	user_info = r.json()
	print json.dumps(user_info)

	# To get the BP information based on access token
	sc_BP = "&sc=89ec14345f8948c891ba804a7c3ff68c"
	sv_BP = "&sv=760428253c7e4fe7ade76580052d2c08"
	print_header("Requesting BP Information")
	url = "https://api.ihealthlabs.com:8443/openapiv2/user/" + user_id + "/bp.json/?" + client_id + client_secret + redirect_uri + "access_token=" + access_token + sc_BP + sv_BP
	# print url
	r = requests.get(url)
	print r
	r_json = r.json()
	print json.dumps(r_json)

	store_BP_information(r_json, user_info)



	return HttpResponse("Get the token!")


@csrf_exempt
def getFitBitHR(request):

	# url = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2288HD&redirect_uri=http://localhost:8000/callbackFitBit/&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight"

	url = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2288HD&redirect_uri=http://a11a9925.ngrok.io/callbackFitBit/&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight"
	
	# r = requests.get(url)
	# print r
	# print r.json()
	return HttpResponseRedirect(url)

@csrf_exempt
def callbackFitBit(request):
	code = request.GET.get('code')
	print "code: " + code
	print "Got the callback from FitBit!"

	# To get the access token based on code
	url = "https://api.fitbit.com/oauth2/token"
	client_id = "2288HD"
	client_secret = "client_secret=0c55f6bb18078641ba19f004c24bdb43&"
	response_type = "response_type=token&"
	# redirect_uri = "http://localhost:8000/callbackFitBit/"
	redirect_uri = "http://a11a9925.ngrok.io/callbackFitBit/"
	data = {
		"code": code,
		"grant_type": "authorization_code",
		"client_id": client_id,
		"redirect_uri": redirect_uri,
		"expires_in": "3600"
	}
	headers = {
		'Authorization': 'Basic MjI4OEhEOjBjNTVmNmJiMTgwNzg2NDFiYTE5ZjAwNGMyNGJkYjQz=', 
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	print_header("Getting Access Token")

	r = requests.post(url = url, data = data, headers = headers)
	# print r
	r_json = r.json()
	# print r_json
	access_token = r_json['access_token']
	user_id = r_json['user_id']

	# To get the Heart Rate information based on access token
	# datetime1 = datetime.datetime.now()
	# endDate = str(datetime1) [0:10]
	# startDate = "2017-04-16"
	date = datetime.datetime.today().strftime('%Y-%m-%d') # "2017-03-10"

	print_header("Getting HR data")
	headers = {
		"Authorization": "Bearer " + access_token,
	}
	# request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/2017-04-12/2017-04-16/1sec.json"
	request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/" + date + "/1d/5min/time/00:00/23:59.json"
	# print request_url
	r = requests.get(url = request_url, headers = headers)
	# print r
	r_json = r.json()
	# print r_json['activities-heart-intraday']['dataset']
	# print json.dumps(r_json['activities-heart-intraday']['dataset'])
	# makePostRequest(r_json['activities-heart-intraday']['dataset'], date)
	# store_HR_information(r_json['activities-heart-intraday']['dataset'], date)

	# To get the step count, calories burnt and miles
	print_header("Getting Step Count data")
	request_url = "https://api.fitbit.com/1/user/-/activities/date/"+ date +" .json"
	r = requests.get(url = request_url, headers = headers)
	# print r
	r_json = r.json()
	# print json.dumps(r_json)
	# store_activity_information(r_json, date)

	# To get the current heartrate
	print_header("Getting Current HR data")
	request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json"
	r = requests.get(url = request_url, headers = headers)
	r_json = r.json()
	print json.dumps(r_json)
	store_current_HR(r_json)
	return HttpResponse("Success!")


def makePostRequest(data_json, date):
	data = {}
	for obj in data_json:
		ts = datetime.datetime.now()
		tsnow = ts.strftime("%Y-%m-%d %H:%M:%S")
		data['heart_rate'] = obj['value']
		data['device_id'] = "11011"
		data['geo_country'] = "USA"
		data['gender'] = "MALE"
		data['device_type'] = "fitbit"
		data['age'] = 24
		data['timeStamp'] = tsnow #time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S,%f").timetuple())
		print "timestamp start"
		print ts
		print "timestamp end"
		url = "http://Sample-env.hvzfmm2x2u.us-west-1.elasticbeanstalk.com/rest/data/push"
		headers = {'Content-Type': 'application/json'}
		r = requests.post(url=url, data=json.dumps(data), headers=headers)
		print r

def store_current_HR(data_json):
	try:
		current_info = CurrentHRInformation.objects.get(
			heart_rate = data_json['activities-heart'][0]['value']['restingHeartRate'],
			date_time = data_json['activities-heart'][0]['dateTime']
			)
		print current_info
	except:
		try:
			newCurrentHRInformation = CurrentHRInformation(
			heart_rate = data_json['activities-heart'][0]['value']['restingHeartRate'], 
			date_time = data_json['activities-heart'][0]['dateTime'])
			newCurrentHRInformation.save()
		except:
			print "No Current HR Available!"
		
		print "No current HR found!"


def store_activity_information(data_json, date):
	try:
		obj = DailyActivityInformation.get(date = date)
		if obj.steps != data_json['summary']['steps'] or obj.calories != data_json['summary']['caloriesOut'] or obj.distance != data_json['summary']['distances'][0]['distance']:
			obj.steps = data_json['summary']['steps']
			obj.calories = data_json['summary']['caloriesOut']
			obj.distance = data_json['summary']['distances'][0]['distance']
			obj.save()
		obj = DailyActivityInformation.get(steps = data_json['summary']['steps'], calories = data_json['summary']['caloriesOut'], distance = data_json['summary']['distances'][0]['distance'], date = date)
		print "activity information already exists!"
	except:
		try:
			newDailyActivityInformation = DailyActivityInformation.objects.create(
				steps = data_json['summary']['steps'],
				calories = data_json['summary']['caloriesOut'],
				distance = data_json['summary']['distances'][0]['distance'],
				date = date)
		except:
			print "not unique"

		print "New activity information saved!"

def store_HR_information(data_json, date):
	user_info = UserInformation.objects.get(userid = "699ccacbe63b4030826c8a32349f2e3e")

	for obj in data_json:
		try:
			prev_HR = HRDataInformation.objects.get(date = date, time = str(obj['time']), value = obj['value'])
		except:
			newHRDataInformation = HRDataInformation(
				date = date,
				value = obj['value'],
				time = obj['time'],
				user = user_info)
			newHRDataInformation.save()
	print("new HR information saved!")

def store_user_information(data_json):
	try:
		obj = UserInformation.objects.get(userid = data_json['userid'])
		obj.weight=data_json['weight']
		obj.height=data_json['height']
		obj.dateofbirth=data_json['dateofbirth']
		obj.gender=data_json['gender']
		obj.userid=data_json['userid']
		obj.WeightUnit=data_json['WeightUnit']
		obj.HeightUnit=data_json['HeightUnit']
		obj.nickname=data_json['nickname']

		obj.save()
 		return obj
	except:
		newUserInformation = UserInformation(
			weight=data_json['weight'],
			height=data_json['height'],
			dateofbirth=data_json['dateofbirth'],
			gender=data_json['gender'],
			userid=data_json['userid'],
			WeightUnit=data_json['WeightUnit'],
			HeightUnit=data_json['HeightUnit'],
			nickname=data_json['nickname'])

		newUserInformation.save()
		return newUserInformation
	

def store_BP_information(data_json, user_info):
	
	user_id = store_user_information(user_info)
	print "user information saved!"

	try:
		obj = BPInformation.objects.get(user = user_id, NextPageUrl=data_json['NextPageUrl'],
				CurrentRecordCount=data_json['CurrentRecordCount'], RecordCount=data_json['RecordCount'],
				BPUnit=data_json['BPUnit'], PageLength=data_json['PageLength'], PrevPageUrl=data_json['PrevPageUrl'],
				PageNumber=data_json['PageNumber'])

		obj.NextPageUrl=data_json['NextPageUrl']
		obj.CurrentRecordCount=data_json['CurrentRecordCount']
		obj.RecordCount=data_json['RecordCount']
		obj.BPUnit=data_json['BPUnit']
		obj.PageLength=data_json['PageLength']
		obj.PrevPageUrl=data_json['PrevPageUrl']
		obj.PageNumber=data_json['PageNumber']
		obj.user = user_id
		obj.save()
		print "Already exists BP Information Saved!"

		storeBPDataList(obj, data_json)

	except:
		newBPInformation = BPInformation(
			NextPageUrl=data_json['NextPageUrl'],
			CurrentRecordCount=data_json['CurrentRecordCount'],
			RecordCount=data_json['RecordCount'],
			BPUnit=data_json['BPUnit'],
			PageLength=data_json['PageLength'],
			PrevPageUrl=data_json['PrevPageUrl'],
			PageNumber=data_json['PageNumber'],
			user = user_id)

		newBPInformation.save()
		print "New BP Information saved!"
		storeBPDataList(newBPInformation, data_json)

def storeBPDataList(newBPInformation, data_json):
	for BPData in data_json['BPDataList']:
		try:
			obj = BPDataList.objects.get(DataID = BPData['DataID'])
			obj.MDate = BPData['MDate']
			obj.LastChangeTime = BPData['LastChangeTime']
			obj.HR = BPData['HR']
			obj.HP = BPData['HP']
			obj.Lon = BPData['Lon']
			obj.BPL = BPData['BPL']
			obj.time_zone = BPData['time_zone']
			obj.Note = BPData['Note']
			obj.measurement_time = BPData['measurement_time']
			obj.DataSource = BPData['DataSource']
			obj.LP = BPData['LP']
			obj.Lat = BPData['Lat']
			obj.TimeZone = BPData['TimeZone']
			obj.IsArr = BPData['IsArr']
			obj.save()
			print "Already exists BP Datalist Saved!"

		except:
			newBPDataList = BPDataList(
				DataID = BPData['DataID'], 
				MDate = BPData['MDate'], 
				LastChangeTime = BPData['LastChangeTime'], 
				HR = BPData['HR'], 
				HP = BPData['HP'],
				Lon = BPData['Lon'],
				BPL = BPData['BPL'],
				time_zone = BPData['time_zone'],
				Note = BPData['Note'],
				measurement_time = BPData['measurement_time'],
				DataSource = BPData['DataSource'],
				LP = BPData['LP'],
				Lat = BPData['Lat'],
				TimeZone = BPData['TimeZone'],
				IsArr = BPData['IsArr'],
				bpInformation = newBPInformation)

			newBPDataList.save()
			print "New BP Datalist saved!"

def print_header(message):
	print "**************************************************************************************************"
	print "                                   " + message + "                                                "
	print "**************************************************************************************************"




