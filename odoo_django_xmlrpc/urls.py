from django.conf.urls import url
from django.contrib import admin
 
from odoo_django_xmlrpc.views import (PartnersList,
	) 
 
app_name = "odoo_django"

urlpatterns = [
	url(r'^$', PartnersList.as_view(), name='partners_list')
]
