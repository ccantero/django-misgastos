from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from expensesapp import forms
from expensesapp.models import Expense
from budgetsapp.models import Budget

from django.http import JsonResponse

from django.db.models import Count

from django.core.exceptions import PermissionDenied

# Create your views here.
class CreateExpense(LoginRequiredMixin,generic.CreateView):
	form_class = forms.ExpenseForm
	model = Expense

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.budget = Budget.objects.get(pk=self.kwargs.get('pk'))
		self.object.amount = round(self.object.amount, 2)

		querySet = Expense.objects.filter(name__iexact=self.object.name).filter(budget__exact=self.object.budget)
		if len(querySet) > 0:
			form.add_error("name", 'Ya existe un gasto con este nombre')
			return super().form_invalid(form)	

		self.object.save()
		return super().form_valid(form)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	all_expenses = Expense.objects.all()
	 	most_common_expenses = Expense.objects.values('name').annotate(number_of_entries=Count('name')).order_by('-number_of_entries')[:5]
	 	#most_common_expenses = Expense.objects.annotate(number_of_entries=Count('name')).order_by('number_of_entries')

	 	common_expenses = []

	 	for common_expense in most_common_expenses:
	 		for expense in all_expenses:
	 			if expense.name == common_expense['name']:
	 				common_expenses.append(expense)
	 				break
	 	

	 	context['common_expenses'] = common_expenses[:5]

	 	return context


class UpdateExpense(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
	form_class = forms.ExpenseForm
	model = Expense		
	exclude = ('budget',)

	def test_func(self):
		expenses = Expense.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(expenses) == 1:
			myexpense = expenses[0]

			if myexpense.budget.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

class DeleteExpense(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
	model = Expense
	#select_related = ('user','group')
	success_url = reverse_lazy('home')

	def test_func(self):
		expenses = Expense.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(expenses) == 1:
			myexpense = expenses[0]

			if myexpense.budget.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs.get('pk'))

	# TODO: Fix this! 20210329
	def get_success_url__(self):
		next_url = self.request.POST.get('next', 'home')
		print(next_url)
		return HttpResponseRedirect(next_url)
		#return reverse_lazy(next_url)
		#return reverse(next_url)

	def delete(self,*args,**kwargs):
		#messages.success(self.request,'Post Deleted')

		return super().delete(*args,**kwargs)

import time
from django.http import HttpResponseForbidden

def pay_expense(request):
	if not request.user.is_authenticated:
		return HttpResponseForbidden()

	myid = request.POST['myid']
	if myid == -1:
		data = {
			'ajax_answer': False
		}
	else:
		currentExpense = Expense.objects.get(pk=myid)

		if currentExpense.budget.user.username != request.user.username:
			return HttpResponseForbidden()

		currentExpense.cantidad_pendiente -= 1
		currentExpense.save()

		data = {
				'ajax_answer': True,
				'cantidad_pendiente': currentExpense.cantidad_pendiente
		}

	return JsonResponse(data)