from django.conf.urls import url
from django.urls import path
from telegramapi import views

app_name = 'telegramapi'

urlpatterns = [
	path('listener/',views.listener,name='listener'),
	path('test_speaker/<int:chat_id>/',views.test_speaker,name='test_speaker'),
]