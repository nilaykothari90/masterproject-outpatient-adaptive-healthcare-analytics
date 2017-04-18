from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^getdata/', views.getData),
	url(r'^callbackFitBit/', views.callbackFitBit),
	url(r'^getfitbithr/', views.getFitBitHR),
    url(r'^request/', views.index),
    url(r'^callback/', views.callback)
]