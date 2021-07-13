from django.shortcuts import render

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from investmentapp.models import Invest
from investmentapp import forms

# Create your views here.
class CreateInvestment(LoginRequiredMixin,generic.CreateView):
	#fields = ['name','amount','initial_rate', 'factor']
	model = Invest
	form_class = forms.InvestForm

	def form_valid(self,form):			
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)


class ListInvestment(LoginRequiredMixin,generic.ListView):
	model = Invest

	def get_queryset(self):
		queryset = super().get_queryset()
		# Fix for django.db.utils.ProgrammingError: can't adapt type 'SimpleLazyObject'
		myuser = str(self.request.user)
		return queryset.filter(user__username__iexact=myuser).order_by('name')

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	#context['test'] = 'Test Cantero'
	 	return context
