from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, FormView

from loanapp import forms
from loanapp.models import Loan

from investmentapp.models import Conversion

class AboutView(TemplateView):
    template_name = "loanapp/about.html"

class LoanView(FormView):
    model = Loan
    template_name = 'loanapp/loan_form.html'
    form_class = forms.LoanForm
    success_url = "loanapp/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conversion_list = Conversion.objects.filter(name__iexact='UVA')
        if len(conversion_list) == 1:
            uva_conversion = conversion_list[0]

        context['uva'] = uva_conversion.last_quote
        return context

class LoanQueryView(FormView):
    model = Loan
    template_name = 'loanapp/loan_form.html'
    form_class = forms.LoanForm
    success_url = "loanapp/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #conversion_list = Conversion.objects.filter(name__iexact='UVA')
        #if len(conversion_list) == 1:
        #    uva_conversion = conversion_list[0]

        #context['uva'] = uva_conversion.last_quote

        all_conversion_index = Conversion.objects.all()
        for conversion_obj in all_conversion_index:
            if conversion_obj.name == 'UVA':
                context['uva'] = conversion_obj.last_quote

            if conversion_obj.name == 'ARS':
                context['USD_Blue'] = conversion_obj.last_quote

            if conversion_obj.name == 'ARS_USD_Oficial':
                context['USD'] = conversion_obj.last_quote

        if self.request.GET.get('cuota'):
            context['cuota'] = self.request.GET.get('cuota')
        else:
            context['cuota'] = self.kwargs.get('cuota')

        if self.request.GET.get('saldo'):
            context['saldo'] = self.request.GET.get('saldo')
        else:
            context['saldo'] = self.kwargs.get('saldo')
        
        context['conversion_object_list'] = Conversion.objects.exclude(name__contains='BTC').exclude(name__iexact='USDC')

        return context