from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accountsapp'

urlpatterns = [
	path('login/',auth_views.LoginView.as_view(template_name='accountsapp/login.html'), name='login'),
	path('change-password/',auth_views.PasswordChangeView.as_view(template_name='accountsapp/change-password.html', success_url='/'), name='change_password'),
	path('logout/',auth_views.LogoutView.as_view(), name='logout'),
	path('signup/',views.SignUpView.as_view(), name='signup'),
]
