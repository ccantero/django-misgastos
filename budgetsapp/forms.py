from django import forms
from django.utils.text import slugify

from budgetsapp.models import Budget

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('name','description')
        
    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        super().__init__(*args, **kwargs)
        # Cristhian:
        # Label in the HTML
        # Optional
        self.fields['name'].label = 'Nombre'
        self.fields['description'].label = 'Breve descripcion'

    def clean_name(self):
        data = self.cleaned_data['name']
        data = slugify(data)
        #listado = Budget.objects.filter(name__iexact=data)
        listado = Budget.objects.filter(name__iexact=data).filter(user__exact=self.user)
        print(data)
        print(listado)
        if len(listado) > 0:
            raise forms.ValidationError("Ya hay un presupuesto con ese nombre!")

        return data