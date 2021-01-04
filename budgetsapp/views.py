from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from budgetsapp import forms
from budgetsapp.models import Budget
from expensesapp.models import Expense

class ListBudget(LoginRequiredMixin,generic.ListView):
	model = Budget

	def get_queryset(self):
		print("CCANTERO - get_queryset ListBudget - 1")
		queryset = super().get_queryset()
		print("CCANTERO - get_queryset ListBudget - 1" + str(self.request.user))
		return queryset.filter(user__username__iexact=self.request.user).order_by('name')

class CreateBudget(LoginRequiredMixin,generic.CreateView):
	form_class = forms.BudgetForm
	model = Budget

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	budgets = Budget.objects.filter(user__username__iexact=self.request.user).order_by('name')
	 	#context['budgets'] = budgets

	 	return context

	def form_valid(self,form):
		budgets = Budget.objects.filter(user__username__iexact=self.request.user.username).order_by('name')
		BUDGETS_CHOICES = [('0',"----")]
		BUDGETS_CHOICES.extend([ (x+1, budgets[x]) for x in range(0,len(budgets))])
		
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()

		# For copy Expenses from another Budget
		choice = int(form.data['budget_choice'])
		k, previous_budget_name = BUDGETS_CHOICES[choice]
		listado_expenses = Expense.objects.filter(budget__name__iexact=previous_budget_name)
		for expense in listado_expenses:
			new_expense = Expense()
			new_expense.category_id = expense.category_id
			new_expense.name = expense.name
			new_expense.amount = expense.amount
			new_expense.cantidad_total = expense.cantidad_total
			new_expense.cantidad_pendiente = expense.cantidad_pendiente
			new_expense.gasto = expense.gasto
			new_expense.budget = self.object
			new_expense.save()

		return super().form_valid(form)

class UpdateBudget(LoginRequiredMixin,generic.UpdateView):
	form_class = forms.BudgetForm
	model = Budget

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

class DeleteBudget(LoginRequiredMixin,generic.DeleteView):
	model = Budget
	success_url = reverse_lazy('presupuestos:all')
	#select_related = ('user','group')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs.get('pk'))

	def delete(self,*args,**kwargs):
		messages.success(self.request,'Budget Deleted')
		budgets = Budget.objects.filter(pk__iexact=self.kwargs.get('pk')).order_by('name')
		if len(budgets) > 0:
			for expense in budgets[0].expenses.all():
				expense.delete()

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
	 	if self.object.expired_date != None:
	 		fecha = self.object.expired_date - timezone.now().date()
	 		balance = ingresos - egresos
	 		context['days_left'] = fecha.days
	 		if balance > 0:
	 			context['balance'] = round(balance / fecha.days,2)
	 		else:
	 			context['balance'] = 0
	 	else:
	 		context['days_left'] = ""

	 	return context

class BudgetDetailTiny(LoginRequiredMixin, generic.DetailView):
	model = Budget
	template_name = 'budgetsapp/budget_detail_summary.html'

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk__iexact=self.kwargs.get('pk'))

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	expenses = Expense.objects.filter(budget=self.kwargs.get('pk'))
	 	ingresos = 0
	 	egresos = 0
	 	non_paid_expenses = Expense.objects.filter(budget=self.kwargs.get('pk')).filter(cantidad_pendiente__gt=0)
	 	for expense in expenses:
	 		if expense.gasto == True:
	 			egresos += expense.amount
	 		else:
	 			ingresos += expense.amount

	 	context['egresos'] = egresos
	 	context['ingresos'] = ingresos
	 	if self.object.expired_date != None:
	 		fecha = self.object.expired_date - timezone.now().date()
	 		balance = ingresos - egresos
	 		context['days_left'] = fecha.days
	 		if balance > 0:
	 			context['balance'] = round(balance / fecha.days,2)
	 		else:
	 			context['balance'] = 0
	 	else:
	 		context['days_left'] = ""

	 	context['non_paid_expenses'] = non_paid_expenses

	 	return context
