import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'misgastos.settings')
django.setup()


from django.contrib.auth.models import User

list_user = User.objects.filter(username__iexact='admin')
admin_user = list_user[0]

from categoriesapp.models import Category
from expensesapp.models import Expense

categorias = []
categorias.append('Gastos Medicos')
categorias.append('Tarjeta de Crédito')
categorias.append('Ingresos')
categorias.append('Impuestos')
categorias.append('Automovil')

gastos = []
gastos.append(('Sueldo','Ingresos'))
gastos.append(('Gas Natural','Impuestos'))
gastos.append(('Celular','Impuestos'))
gastos.append(('Edenor','Impuestos'))
gastos.append(('Seguro','Automovil'))

for categoria in categorias:
	if len(Category.objects.filter(name__exact=categoria)) == 0:
		category = Category()
		category.name = categoria
		category.user = admin_user
		category.save()

for (gasto, categoria) in gastos:
	if len(Expense.objects.filter(name__exact=gasto)) == 0:
		categorias = Category.objects.filter(name__exact=categoria)
		category = categorias[0]
		expense = Expense()
		expense.name = gasto
		expense.category = category
		expense.amount = 0
		expense.save()
