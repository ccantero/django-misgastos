from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from categoriesapp.models import Category
from budgetsapp.models import Budget

# Create your views here.
class CreateCategory(LoginRequiredMixin,generic.CreateView):
	fields = ['name', 'description']
	model = Category

	def post(self, request, *args, **kwargs):
		super().post(request,*args,**kwargs)
		next = request.POST.get('next', '/')
		return HttpResponseRedirect(next)

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	context['HTTP_REFERER'] = self.request.META.get('HTTP_REFERER')
	 	return context

	def form_valid(self,form):			
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)	