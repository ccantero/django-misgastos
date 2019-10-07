from django.urls import path
from categoriesapp import views

app_name = 'categorias'

urlpatterns = [
	path('create/',views.CreateCategory.as_view(),name='create'),
]