from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
import xmlrpc
from xmlrpc import client
from accounts.odoo_services.partner_services import PartnerServices
from django.forms import widgets

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','name':'username','placeholder':'Enter username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','name':'pass','placeholder':'Password is required'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':' form-control','name':'email','placeholder':'Enter Email Address'}), required=True)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')

        #Django checking
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not  active')
        
        # Odoo checking
        # if email and username:
        #     db="inimov_test_db"
        #     username=email
        #     url="http://localhost:8069"
        #     try:
        #         common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        #         uid = common.authenticate(db, username, password, {})
        #         if not uid:
        #             uid = common.authenticate(db, email, password, {})
        #     except Exception:
        #         raise forms.ValidationError('Sorry an Error Occured while connecting to oddo')
        #     if not uid:
        #         raise forms.ValidationError('Could not connect to Odoo. Please make sure you provided odoo account credentials')
        
        return  super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email Adress",widget=forms.EmailInput(attrs={'class': 'form-control contatct-form'}))
    email2 = forms.EmailField(label="Confirm email",widget=forms.EmailInput(attrs={'class': 'form-control contatct-form'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), required=True)

    COUNTRIES=[]
    odoo = PartnerServices(username="gregory.goufan@gmail.com",password="Goufan2017")
    odoo.authenticateUser()
    country_dic = odoo.getCountriesIds()
    for country in country_dic:
        COUNTRIES.append([country['id'],country['name']])
    country = forms.CharField(label='Country',max_length=4,min_length=2,empty_value='----',widget=forms.Select(attrs={'class':'form-control'},choices=COUNTRIES))
    phone = forms.IntegerField(widget=forms.TimeInput(attrs={'class': 'form-control contatct-form'}))
    website = forms.CharField(label="Website",widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label="User Name",widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'country',
            'password',
            'phone',
            'website',
        ]
    def clean(self,  *args, **kwargs):
        email = self.cleaned_data['email']
        email2 = self.cleaned_data['email2']
        if email != email2:
            raise forms.ValidationError('emails must match')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already been used')
        return super(UserRegisterForm, self).clean(*args, **kwargs)