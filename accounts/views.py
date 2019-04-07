from django.shortcuts import render, redirect
from django.urls import reverse 
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

import xmlrpc
from xmlrpc import client
from decouple import config

# Create your views here.

from .forms import  UserLoginForm, UserRegisterForm
from accounts.odoo_services.partner_services import PartnerServices

def login_view(request):
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    print('\nIn login is form valid',form.is_valid())
    if request.method=='POST':
        print('\nform.username',form.data['username'])
        print('\nform.password',form.data['password'])
        print('\nform.email',form.data['email'])
    if form.is_valid():
        print('\nIn is_valid no errors')
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        if _next:
            return redirect(_next)
        return redirect('/')
    context = {
        "form":form
    }

    return render(request, "accounts/login.html",context)

def register_view(request):
    _next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        #Django Registration
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.set_password(password)

        phone = form.cleaned_data.get('phone')
        website = form.cleaned_data.get('website')
        country_id = form.cleaned_data.get('country')

        #Odoo New Partner Create
        
        print('\nname',username)
        print('\npassword',password)
        print('\nphone',phone)
        print('\nwebsite',website)
        print('\ncountry_id',country_id)
        print('\nemail',user.email)
        print('\npassword',password)
        print('\nphone',phone)
        print('\nwebsite',website)
        print('\ncountry_id',country_id)
        print('\nemail',user.email)
        partnerRow = [{"name":username,"password":password,"phone":phone,"website":website,"country_id":country_id,"email":user.email}]
        try:
            odoo = PartnerServices(username=config('USER'),password=config('DB_PASSWORD'))
            odoo.authenticateUser()
            is_saved_on_odoo = odoo.partnerAdd(partnerRow)
            if not is_saved_on_odoo:
                messages.error(request, 'A problem occured couldn\'t create user on odoo.')
                return redirect('/accounts/register/')
        except Exception as e:
            messages.error(request, 'An Error Occured while saving a New Odoo User.')
            print(e)
            return redirect(reverse('accounts/register/'))

        #commit django and odoo registration
        
        user.save()
        new_user = authenticate(username=user.username, password=password)
        if not new_user:
            messages.error(request, 'A problem occured couldn\'t create user on django.')
            return redirect(reverse('accounts/register/'))
        login(request, new_user)        
        messages.success(request, 'User with email address '+user.email+' created.')
        # return redirect(reverse('odoo_django:partners_list'))
        if _next:
            return redirect(_next)
        return redirect('/')
    context = {
        "form":form
    }

    return render(request, "accounts/signup.html",context)

def logout_view(request):
    logout(request)
    return redirect('/')

