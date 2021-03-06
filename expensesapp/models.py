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
	amount = models.FloatField()
	cantidad_total = models.PositiveIntegerField(default=1)
	cantidad_pendiente = models.PositiveIntegerField(default=0)
	gasto = models.BooleanField(default=True)
	tarjeta_credito = models.BooleanField(default=False)
	budget = models.ForeignKey(Budget,related_name='expenses',null=True, blank=True,on_delete=models.PROTECT)
	skip = models.BooleanField(default=False)

	@property
	def total_amount(self):
		return round(self.amount * self.cantidad_total, 2)

	@property
	def pending_amount(self):
		return round(self.amount * self.cantidad_pendiente,2)

	@property
	def is_paid(self):
		return self.cantidad_pendiente == 0

	@property
	def get_amount(self):
		return self.total_amount - self.pending_amount

	@property
	def is_credit_card(self):
		return self.tarjeta_credito

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('presupuestos:detail',kwargs={'pk':self.budget.pk})

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)