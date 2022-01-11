from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from budgetsapp import forms
from budgetsapp.models import Budget
from expensesapp.models import Expense

from django.core.exceptions import PermissionDenied

class ListBudget(LoginRequiredMixin,generic.ListView):
	model = Budget

	def get_queryset(self):
		queryset = super().get_queryset()
		# Fix for django.db.utils.ProgrammingError: can't adapt type 'SimpleLazyObject'
		myuser = str(self.request.user)
		return queryset.filter(user__username__iexact=myuser).order_by('-expired_date')

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
		if choice == 0:
			return super().form_valid(form)

		k, previous_budget = BUDGETS_CHOICES[choice]
		previous_budget_name = previous_budget.name
		budgets_list = Budget.objects.filter(user__username__iexact=self.request.user.username).filter(name__iexact=previous_budget_name)
		mybudget = budgets_list[0]

		#listado_expenses = Expense.objects.filter(budget__name__iexact=previous_budget_name)
		listado_expenses = Expense.objects.filter(budget__pk__exact=mybudget.pk)

		for expense in listado_expenses:
			new_expense = Expense()
			new_expense.category_id = expense.category_id
			new_expense.name = expense.name
			new_expense.amount = expense.amount
			new_expense.tarjeta_credito = expense.tarjeta_credito
			new_expense.cantidad_total = expense.cantidad_total
			new_expense.cantidad_pendiente = expense.cantidad_total
			new_expense.skip = False
			if new_expense.tarjeta_credito:
				if expense.cantidad_total == 1:
					new_expense.skip = True
				elif expense.cantidad_pendiente > 0:
					new_expense.cantidad_pendiente = expense.cantidad_pendiente - 1 
				elif expense.cantidad_total > 1:
					continue

			new_expense.gasto = expense.gasto
			new_expense.budget = self.object
			new_expense.save()

		return super().form_valid(form)

class UpdateBudget(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
	form_class = forms.BudgetForm
	model = Budget

	def test_func(self):
		budgets = Budget.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(budgets) == 1:
			mybudget = budgets[0]

			if mybudget.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

class DeleteBudget(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
	model = Budget
	success_url = reverse_lazy('presupuestos:all')
	#select_related = ('user','group')

	def test_func(self):
		budgets = Budget.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(budgets) == 1:
			mybudget = budgets[0]
			
			if mybudget.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs.get('pk'))

	def delete(self,*args,**kwargs):
		messages.success(self.request,'Budget Deleted')
		budgets = Budget.objects.filter(pk__exact=self.kwargs.get('pk')).order_by('name')
		if len(budgets) > 0:
			for expense in budgets[0].expenses.all():
				expense.delete()

		return super().delete(*args,**kwargs)

class BudgetDetail(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
	model = Budget

	def test_func(self):
		budgets = Budget.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(budgets) == 1:
			mybudget = budgets[0]
			
			if mybudget.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk__exact=self.kwargs.get('pk'))

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	expenses = Expense.objects.filter(budget=self.kwargs.get('pk'))
	 	ingresos = 0
	 	egresos = 0
	 	tarjeta_credito = 0
	 	for expense in expenses:
	 		if expense.skip:
	 			continue

	 		if expense.gasto == True:
	 			if expense.tarjeta_credito == False:
	 				egresos += expense.pending_amount
	 			else:
	 				if expense.is_paid:
	 					tarjeta_credito += round(expense.amount)
	 				else:
	 					tarjeta_credito += expense.pending_amount
	 		else:
	 			ingresos += expense.amount

	 	context['egresos'] = round(egresos,2)
	 	context['ingresos'] = round(ingresos,2)
	 	context['tarjeta_credito'] = round(tarjeta_credito,2)

	 	if self.object.expired_date != None:
	 		fecha = self.object.expired_date - timezone.now().date()
	 		balance = ingresos - egresos
	 		context['days_left'] = fecha.days
	 		if balance > 0:
	 			if fecha.days > 0:
	 				context['balance'] = round(balance / fecha.days,2)
	 			else:
	 				context['balance'] = round(balance,2)
	 		else:
	 			context['balance'] = 0
	 	else:
	 		context['days_left'] = ""

	 	return context

class BudgetDetailTiny(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
	model = Budget
	template_name = 'budgetsapp/budget_detail_summary.html'

	def test_func(self):
		budgets = Budget.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(budgets) == 1:
			mybudget = budgets[0]
			
			if mybudget.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk__exact=self.kwargs.get('pk'))

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	expenses = Expense.objects.filter(budget=self.kwargs.get('pk'))
	 	ingresos = 0
	 	egresos = 0
	 	tarjeta_credito = 0
	 	egresos_pendientes = 0
	 	non_paid_expenses = Expense.objects.filter(budget=self.kwargs.get('pk')).filter(cantidad_pendiente__gt=0).filter(tarjeta_credito=False).filter(skip=False)
	 	for expense in expenses:
	 		if expense.skip:
	 			continue
	 			
	 		if expense.gasto == True:
 				if expense.tarjeta_credito == False:
	 				egresos += expense.get_amount
	 				egresos_pendientes += expense.pending_amount
	 			else:
	 				tarjeta_credito += expense.get_amount
	 		else:
	 			ingresos += expense.get_amount

	 	context['egresos'] = round(egresos, 2)
	 	context['ingresos'] = round(ingresos, 2)
	 	if self.object.expired_date != None:
	 		fecha = self.object.expired_date - timezone.now().date()
	 		balance = ingresos - egresos - egresos_pendientes
	 		context['days_left'] = fecha.days
	 		if balance > 0:
	 			if fecha.days > 0:
	 				context['balance'] = round(balance / fecha.days,2)
	 			else:
	 				context['balance'] = round(balance,2)
	 		else:
	 			context['balance'] = 0
	 	else:
	 		context['days_left'] = ""

	 	context['non_paid_expenses'] = non_paid_expenses
	 	context['egresos_pendientes'] = round(egresos_pendientes, 2)

	 	return context
