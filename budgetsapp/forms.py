from django import forms
from django.utils.text import slugify

from budgetsapp.models import Budget

#from django.contrib.admin.widgets import AdminDateWidget

class BudgetForm(forms.ModelForm):
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

    def clean_name(self):
        data = self.cleaned_data['name']
        data = slugify(data)
        listado = Budget.objects.filter(slug__iexact=data).filter(user__exact=self.user)
        if len(listado) > 0 and self.cleaned_data['name'] != self.instance.name:
            raise forms.ValidationError("Ya hay un presupuesto con ese nombre!")

        return data