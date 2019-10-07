from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from budgetsapp.models import Budget
from expensesapp.models import Expense

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms

class ListBudget(LoginRequiredMixin,generic.ListView):
	model = Budget

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(user__username__iexact=self.request.user)


class CreateBudget(LoginRequiredMixin,generic.CreateView):
	form_class = forms.BudgetForm
	model = Budget

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

class UpdateBudget(LoginRequiredMixin,generic.UpdateView):
	form_class = forms.BudgetForm
	model = Budget		

class DeleteBudget(LoginRequiredMixin,generic.DeleteView):
	model = Budget
	#select_related = ('user','group')
	success_url = reverse_lazy('presupuestos:all')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs.get('pk'))

	def delete(self,*args,**kwargs):
		messages.success(self.request,'Budget Deleted')
		return super().delete(*args,**kwargs)

class BudgetDetail(LoginRequiredMixin, generic.DetailView):
	model = Budget

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk__iexact=self.kwargs.get('pk'))

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	expenses = Expense.objects.filter(budget=self.kwargs.get('pk'))
	 	ingresos = 0
	 	egresos = 0
	 	for expense in expenses:
	 		if expense.gasto == True:
	 			egresos += expense.amount
	 		else:
	 			ingresos += expense.amount

	 	context['egresos'] = egresos
	 	context['ingresos'] = ingresos
	 	return context