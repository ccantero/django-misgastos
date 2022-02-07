from django import forms

from .models import Loan

class LoanForm(forms.ModelForm):

    class Meta:
        model = Loan
        fields = ('amount_cuota','amount_deuda')


    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_cuota'].label = 'Monto Cuota ( UVA )'
        self.fields['amount_deuda'].label = 'Monto Deuda ( UVA )'