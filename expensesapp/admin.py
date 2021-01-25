from django.contrib import admin1

from expensesapp import models

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'cantidad_total', 'cantidad_pendiente', 
    				'gasto', 'tarjeta_credito')

admin.site.register(models.Expense, ExpenseAdmin)