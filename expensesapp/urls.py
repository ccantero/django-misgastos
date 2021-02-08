from django.conf.urls import url
from django.urls import path
from expensesapp import views

app_name = 'gastos'

urlpatterns = [
	path('update/<int:pk>/',views.UpdateExpense.as_view(),name='update_expense'),
	path('delete/<int:pk>/',views.DeleteExpense.as_view(),name='delete_expense'),
	path('ajax/validate_username/',views.update_expense,name='validate_username'),
	#path('create/',views.CreateExpense.as_view(),name='_create_'),
	#path('expense/create/',views.CreateExpense.as_view(),name='create_expense'),
	#path('<int:pk>/',views.BudgetDetail.as_view(),name='detail'),

]