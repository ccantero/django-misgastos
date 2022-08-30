from django.urls import path
from loanapp import views

app_name = 'loans'

urlpatterns = [
	path('',views.AboutView.as_view()),
	path('test',views.LoanView.as_view()),
	path('calculadora_uva/',views.LoanQueryView.as_view(), {'cuota':0, 'saldo':0}, name='calculadora'),
	path('clear-cookies', views.clear_cookies),
]