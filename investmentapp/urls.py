from django.urls import path
from investmentapp import views

app_name = 'inversiones'

urlpatterns = [
	path('',views.ListInvestment.as_view(),name='all'),
	path('create/',views.CreateInvestment.as_view(),name='create'),
	path('update/<int:pk>/',views.UpdateInvestment.as_view(),name='update'),
	path('delete/<int:pk>/',views.DeleteInvestment.as_view(),name='delete'),
]