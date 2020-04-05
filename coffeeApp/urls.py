from django.conf.urls import url
from django.urls import path
from coffeeApp import views

app_name = 'coffee'

urlpatterns = [
	path('',views.CoffeeList.as_view(),name='all'),
	path('json/',views.CoffeeListJSON.as_view(),name='all_json'),
	path('<int:pk>',views.CoffeeDetail.as_view(),name='single'),
	path('<int:pk>.json',views.CoffeeDetailJSON.as_view(),name='single_json'),
]