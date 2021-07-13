from django import forms

from .models import Invest, Conversion

class InvestForm(forms.ModelForm):

    class Meta:
        model = Invest
        fields = ('name','amount','initial_rate', 'factor')
        
    def __init__(self,*args,**kwargs):
        #self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        super().__init__(*args, **kwargs)
        self.fields["factor"].queryset = (
                     Conversion.objects.filter(
                      active_for_selection__exact=True
                  ).order_by('name')
        )