from django.shortcuts import render
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime

from auth2.models import BPInformation, BPDataList, UserInformation, HRDataInformation
# Create your views here.
@csrf_exempt
def index(request):

	url = "https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?client_id=685895e7db4d420799808416d8fbb95b&response_type=code&redirect_uri=http://localhost:8000/callback/&APIName=OpenApiBP"
	# url = "https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?"
	headers = {
		'client_id':'685895e7db4d420799808416d8fbb95b',
		'response_type':'code',
		'redirect_uri':'http://yourcallback.com',
		'APIName':'OpenApiBP'
	}
	print_header("Getting Code")
	r = requests.get(url)
	print r
	# print r.json()
	return HttpResponseRedirect(url)

@csrf_exempt
def getData(request):
	user_info = UserInformation.objects.get(userid = "699ccacbe63b4030826c8a32349f2e3e")
	print user_info.id
	bp_info = BPInformation.objects.get(user = user_info.id)
	bpdata_info = bp_info.objects.get(bpInformation = bp_info.id)
	hr_info = HRDataInformation.objects.get(userid = "699ccacbe63b4030826c8a32349f2e3e")
	return HttpResponse("Data Send!")

@csrf_exempt
def callback(request):
	code = request.GET.get('code')
	print "code: " + code
	print "Got the callback!"

	client_id = "client_id=685895e7db4d420799808416d8fbb95b&"
	client_secret = "client_secret=6b633671d03f4e43a7d9a55e4ddeb9fd&"
	grant_type = "grant_type=authorization_code&"
	redirect_uri = "redirect_uri=http://localhost:8000/callback/&"
	url = "https://api.ihealthlabs.com:8443/OpenApiV2/OAuthv2/userauthorization/?" + client_id + client_secret + grant_type + redirect_uri + "code=" + code
	print_header("Getting Token")
	r = requests.get(url)
	r_json = r.json()
	print r
	print r_json
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
	print r_json
	access_token = r_json['AccessToken']

	
	# To get the User information based on access token
	sc_user_info = "&sc=89ec14345f8948c891ba804a7c3ff68c"
	sv_user_info = "&sv=9823bbc6f2904b0fad40bb32c9dd4b2c"
	print_header("Requesting User Information")
	url = "https://api.ihealthlabs.com:8443/openapiv2/user/" + user_id + ".json/?" + client_id + client_secret + redirect_uri + "access_token=" + access_token + sc_user_info + sv_user_info + "&locale=en_US"
	print url
	r = requests.get(url)
	print r
	user_info = r.json()
	print json.dumps(user_info)

	# To get the BP information based on access token
	sc_BP = "&sc=89ec14345f8948c891ba804a7c3ff68c"
	sv_BP = "&sv=760428253c7e4fe7ade76580052d2c08"
	print_header("Requesting BP Information")
	url = "https://api.ihealthlabs.com:8443/openapiv2/user/" + user_id + "/bp.json/?" + client_id + client_secret + redirect_uri + "access_token=" + access_token + sc_BP + sv_BP
	print url
	r = requests.get(url)
	print r
	r_json = r.json()
	print json.dumps(r_json)

	store_BP_information(r_json, user_info)

	return HttpResponse("Get the token!")


@csrf_exempt
def getFitBitHR(request):

	url = "https://www.fitbit.com/oauth2/authorize?response_type=code&client_id=2288HD&redirect_uri=http://localhost:8000/callbackFitBit/&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight"
	
	r = requests.get(url)
	print r
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
	redirect_uri = "http://localhost:8000/callbackFitBit/"
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

	r = requests.post(url=url,data=data,headers=headers)
	print r
	r_json = r.json()
	print r_json
	access_token = r_json['access_token']
	user_id = r_json['user_id']

	# To get the Heart Rate information based on access token
	datetime1 = datetime.datetime.now()
	endDate = str(datetime1) [0:10]
	startDate = "2017-04-16"
	date = "2017-04-16"
	print_header("Getting HR data")
	headers = {
		"Authorization": "Bearer " + access_token,
	}
	# request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/2017-04-12/2017-04-16/1sec.json"
	request_url = "https://api.fitbit.com/1/user/-/activities/heart/date/" + date + "/1d/1min/time/00:00/23:59.json"
	print request_url
	r = requests.get(url=request_url, headers=headers)
	print r
	r_json = r.json()
	# print r_json['activities-heart-intraday']['dataset']
	# print json.dumps(r_json['activities-heart-intraday']['dataset'])
	# store_HR_information(r_json['activities-heart-intraday']['dataset'], date)
	return HttpResponse("Success!")

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
	print "BP Information saved!"

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

		except:
			BPDataLists123 = BPDataList(
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

			BPDataLists123.save()


def print_header(message):
	print "**************************************************************************************************"
	print "                                   " + message + "                                                "
	print "**************************************************************************************************"




