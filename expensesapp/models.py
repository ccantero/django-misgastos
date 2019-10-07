from django.db import models

# Create your models here.
from django.urls import reverse
from budgetsapp.models import Budget
from categoriesapp.models import Category

class Expense(models.Model):

	querySet = Category.objects.filter(name="Impuestos")
	name = models.CharField(max_length=100)

	if len(querySet) == 0:
		category = models.ForeignKey(	Category,
									related_name='categories',
									on_delete=models.PROTECT)	
	else:
		category = models.ForeignKey(	Category,
										default=querySet[0].pk, # PK for Caterogies
										related_name='categories',
										on_delete=models.PROTECT)

	amount = models.PositiveIntegerField()
	gasto = models.BooleanField(default=True)
	budget = models.ForeignKey(Budget,related_name='expenses',on_delete=models.PROTECT)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('presupuestos:detail',kwargs={'pk':self.budget.pk})

	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)