from django.db import models

# Create your models here.
from django.urls import reverse
from budgetsapp.models import Budget

class Expense(models.Model):
	name = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	amount = models.PositiveIntegerField()
	gasto = models.BooleanField(default=True)
	budget = models.ForeignKey(Budget,related_name='expenses',on_delete=models.PROTECT)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('presupuestos:detail',kwargs={'pk':self.budget.pk})

