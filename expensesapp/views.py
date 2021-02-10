from django.shortcuts import render

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from expensesapp import forms
from expensesapp.models import Expense
from budgetsapp.models import Budget

from django.http import JsonResponse


# Create your views here.
class CreateExpense(LoginRequiredMixin,generic.CreateView):
	form_class = forms.ExpenseForm
	model = Expense

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.budget = Budget.objects.get(pk=self.kwargs.get('pk'))

		self.object.amount = round(self.object.amount, 2)
		self.object.save()
		return super().form_valid(form)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	common_expenses = Expense.objects.all()
	 	context['common_expenses'] = common_expenses

	 	return context


class UpdateExpense(LoginRequiredMixin,generic.UpdateView):
	form_class = forms.ExpenseForm
	model = Expense		
	exclude = ('budget',)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

class DeleteExpense(LoginRequiredMixin,generic.DeleteView):
	model = Expense
	#select_related = ('user','group')
	success_url = reverse_lazy('home')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs.get('pk'))

	def delete(self,*args,**kwargs):
		messages.success(self.request,'Post Deleted')
		return super().delete(*args,**kwargs)

import time

def update_expense(request):
    time. sleep(5) 
    data = {
        'is_taken': True
    }
    return JsonResponse(data)