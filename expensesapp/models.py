from django.db import models

# Create your models here.
from django.urls import reverse
from budgetsapp.models import Budget
from categoriesapp.models import Category

from django.db.utils import OperationalError

class Expense(models.Model):

	category = models.ForeignKey(	Category,
									related_name='categories',
									on_delete=models.PROTECT)	

	name = models.CharField(max_length=100)
	amount = models.PositiveIntegerField()
	cantidad_total = models.PositiveIntegerField(default=1)
	cantidad_pendiente = models.PositiveIntegerField(default=1)
	gasto = models.BooleanField(default=True)
	budget = models.ForeignKey(Budget,related_name='expenses',null=True, blank=True,on_delete=models.PROTECT)

	@property
	def total_amount(self):
		return self.amount * self.cantidad_total

	@property
	def pending_amount(self):
		return self.amount * self.cantidad_pendiente

	@property
	def is_paid(self):
		return self.cantidad_pendiente > 0

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('presupuestos:detail',kwargs={'pk':self.budget.pk})

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)