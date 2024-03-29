"""misgastos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage.as_view(),name='home'),
    path('new/',views.NewHomePage.as_view(),name='new_home'),
    path('accounts/',include('accountsapp.urls',namespace='accounts')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('test/',views.TestPage.as_view(),name='test'),
    path('thanks/',views.ThanksPage.as_view(),name='thanks'),
    path("presupuestos/", include("budgetsapp.urls", namespace="presupuestos")),
    path("gastos/", include("expensesapp.urls", namespace="gastos")),
    path("categorias/", include("categoriesapp.urls", namespace="categorias")),
    path("coffees/", include("coffeeApp.urls", namespace="coffee")),
    path("telegramapi/", include("telegramapi.urls", namespace="telegramapi")),
    path("inversiones/", include("investmentapp.urls", namespace="inversiones")),

    path("loans/", include("loanapp.urls", namespace="loans")),
]