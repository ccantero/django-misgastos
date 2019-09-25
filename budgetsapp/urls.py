from django.conf.urls import url
from django.urls import path
from . import views
from expensesapp import views as expenses_views

app_name = 'presupuestos'

urlpatterns = [
	path('',views.ListBudget.as_view(),name='all'),
	path('create/',views.CreateBudget.as_view(),name='create'),
	path('<int:pk>/gastos/create/',expenses_views.CreateExpense.as_view(),name='create_expense'),
	path('update/<int:pk>/',views.UpdateBudget.as_view(),name='update'),
	path('delete/<int:pk>/',views.DeleteBudget.as_view(),name='delete'),
	path('<int:pk>/',views.BudgetDetail.as_view(),name='detail'),
]