from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
import datetime
from django.contrib import messages
from django.db.models import Sum,Count
from calendar import monthrange
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from .models import Partner

# Create your views here.

# import odoolib
import xmlrpc
from xmlrpc import client
from decouple import config

class PartnersList(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/' 
    # redirect_field_name = '/g-search/revenue_by_customer/'
    # model = Data 
    template_name = 'res/partners_list.html'
    object_list = 'object_list'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['prompt']="Press Submit button to create a new Partner."
        context['xmlrpc'] = xmlrpc
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print('\n\ncontext',context)

        ### All Odoo way of fecthing data are cleaned in partner_services class just I did not wanted to waste time 
        ### and make this code more OO 

        user=config('USER')
        db=config('DB_NAME')
        password=config('DB_PASSWORD')
        port=config('PORT')
        url=config('ODOO_HOST')
        url_common="{}:{}/xmlrpc/2/common".format(url,port)
        url_object="{}:{}/xmlrpc/2/object".format(url,port)
        odoo_common = xmlrpc.client.ServerProxy(url_common)

        common = client.ServerProxy('{}/xmlrpc/2/common'.format("http://localhost:8069"))
        common.version()
  
        uid = common.authenticate(config('DB_NAME'), config('USER'), config('DB_PASSWORD'), {})
        print('\n\nuid:',uid)

        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format("http://localhost:8069"))
        check_access_rights =  models.execute_kw(db, uid, password,'res.partner', 'check_access_rights',['read'], {'raise_exception': False})

        count_ids = models.execute_kw(db, uid, password,
            'res.partner', 'search_count',
            [[['is_company', '=', True], ['customer', '=', True]]])

        ids = models.execute_kw(db, uid, password,
            'res.partner', 'search',[[]])

        partner_list = models.execute_kw(db, uid, password,
            'res.partner', 'read',
            [ids], {'fields': ['name', 'country_id', 'comment','website','email','phone']})

        context['partner_list'] = partner_list

        messages.success(self.request, 'List of Partners reached.')
        # return redirect(reverse('odoo_django:partners_list'))
        return render(request, self.template_name, {"context":context})

    
    def get_queryset(self, **kwargs):
        return Partner.objects.all()
