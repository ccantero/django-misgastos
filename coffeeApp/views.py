from django.shortcuts import render

# Create your views here.
from django.views import generic
from coffeeApp.models import Coffee
from django.http import JsonResponse

from django.core import serializers

class CoffeeListJSON(generic.ListView):
	model = Coffee

	def render_to_response(self, context, **response_kwargs):
		queryset = self.get_queryset().values()
		lista = list(queryset)

		return JsonResponse(lista, **response_kwargs, safe=False)

class CoffeeList(generic.ListView):
	model = Coffee

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset


class CoffeeDetail(generic.DetailView):
	model = Coffee

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk__exact=self.kwargs.get('pk'))

class CoffeeDetailJSON(generic.DetailView):
	model = Coffee

	def render_to_response(self, context, **response_kwargs):
		queryset = super().get_queryset()
		mydata = queryset.filter(pk__exact=self.kwargs.get('pk')).values()
		lista = list(mydata)
		myCoffee = lista[0]
		return JsonResponse(myCoffee, **response_kwargs, safe=False)

