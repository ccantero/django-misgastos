from django import forms
from expensesapp.models import Expense
from budgetsapp.models import Budget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name','category','amount','gasto')
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        # Cristhian:
        # Label in the HTML
        # Optional
        self.fields['name'].label = 'Nombre'
        self.fields['category'].label = 'Categoria'
