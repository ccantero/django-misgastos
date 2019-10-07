from django import forms
from expensesapp.models import Expense
from categoriesapp.models import Category

from django.contrib.auth.models import User

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name','category','amount','gasto')
        
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        super().__init__(*args, **kwargs)
        # Cristhian:
        # Label in the HTML
        # Optional
        query_set = User.objects.filter(username='admin')
        admin_pk = query_set[0].pk
        self.fields['name'].label = 'Nombre'
        self.fields['category'].label = 'Categoria'
        self.fields["category"].queryset = (
                     Category.objects.filter(
                      user__in=[self.user.pk,admin_pk]
                  )
        )
