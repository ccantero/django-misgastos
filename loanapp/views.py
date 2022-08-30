from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, FormView

from loanapp import forms
from loanapp.models import Loan

from investmentapp.models import Conversion

class AboutView(TemplateView):
    template_name = "loanapp/dashboard.html"
    #template_name = "loanapp/about.html"

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

    def _render_to_response(self, context, **response_kwargs):
        response = super(FormView, self).render_to_response(context, **response_kwargs)
        print(context)
        response.set_cookie('CC', 'MyCookie')
        return response

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

        #list_of_cookies = self.request.COOKIES
        #for cookie in list_of_cookies:
        #    print(cookie)

        all_conversion_index = Conversion.objects.all()
        uva_quote = 0.0
        blue_quote = 0.0
        green_quote = 0.0
        for conversion_obj in all_conversion_index:
            if conversion_obj.name == 'UVA':
                context['uva'] = conversion_obj.last_quote
                uva_quote = conversion_obj.last_quote

            if conversion_obj.name == 'ARS':
                context['USD_Blue'] = conversion_obj.last_quote
                blue_quote = conversion_obj.last_quote

            if conversion_obj.name == 'ARS_USD_Oficial':
                context['USD'] = conversion_obj.last_quote
                green_quote = conversion_obj.last_quote

        if self.request.GET.get('cuota') :
            # I have receieved on URL
            context['cuota'] = self.request.GET.get('cuota')
            context['cuota_calculada'] = float(self.request.GET.get('cuota')) * uva_quote
        elif self.request.COOKIES.get('_cuota__') and self.request.COOKIES.get('_cuota__') != "undefined":
            context['cuota'] = self.request.COOKIES.get('_cuota__')
            context['cuota_calculada'] = float(self.request.COOKIES.get('_cuota__')) * uva_quote
        else:
            context['cuota'] = 0.0
            context['cuota_calculada'] = 0.0

        if self.request.GET.get('saldo'):
            # I have receieved on URL
            context['saldo'] = self.request.GET.get('saldo')
            context['saldo_calculado_usd'] = float(self.request.GET.get('saldo')) * uva_quote / green_quote
            context['saldo_calculado_usd_blue'] = float(self.request.GET.get('saldo')) * uva_quote / blue_quote
        elif self.request.COOKIES.get('_deuda__') and self.request.COOKIES.get('_deuda__') != "undefined":
            context['saldo'] = self.request.COOKIES.get('_deuda__')
            context['saldo_calculado_usd'] = float(self.request.COOKIES.get('_deuda__')) * uva_quote / green_quote
            context['saldo_calculado_usd_blue'] = float(self.request.COOKIES.get('_deuda__')) * uva_quote / blue_quote
        else:
            context['saldo'] = 0.0
            context['saldo_calculado_usd'] = 0.0
            context['saldo_calculado_usd_blue'] = 0.0
        
        context['conversion_object_list'] = Conversion.objects.exclude(name__contains='BTC').exclude(name__iexact='USDC')

        return context

from django.http import HttpResponseRedirect
def clear_cookies(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('_deuda__')
    response.delete_cookie('_cuota__')
    return response