from django import forms
from django.utils.text import slugify

from budgetsapp.models import Budget

class BudgetForm(forms.ModelForm):
    budget_choice = forms.ChoiceField()

    class Meta:
        model = Budget
        fields = ('name','description','expired_date')
        
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        super().__init__(*args, **kwargs)
        # Cristhian:
        # Label in the HTML
        # Optional
        self.fields['name'].label = 'Nombre'
        self.fields['description'].label = 'Breve descripcion'
        self.fields['expired_date'].label = 'Fecha de finalizacion'
        self.fields['expired_date'].widget = forms.DateInput(attrs={'class':'datepicker'})
        
        budgets = Budget.objects.filter(user__username__iexact=self.user.username).order_by('name')
        BUDGETS_CHOICES = [(0,"----")]
        #BUDGETS_CHOICES.extend([ (x+1, budgets[x]) for x in range(0,len(budgets)) ])
        BUDGETS_CHOICES.extend([ (x+1, budgets[x]) for x in range(0,len(budgets)) if budgets[x].expenses.all().count() > 0 ])
        self.fields['budget_choice'].label = 'Copiar gastos'
        self.fields['budget_choice'].choices = BUDGETS_CHOICES

    def clean_name(self):
        data = self.cleaned_data['name']
        data = slugify(data)
        listado = Budget.objects.filter(slug__iexact=data).filter(user__exact=self.user)
        if len(listado) > 0 and self.cleaned_data['name'] != self.instance.name:
            raise forms.ValidationError("Ya hay un presupuesto con ese nombre!")

        return data
