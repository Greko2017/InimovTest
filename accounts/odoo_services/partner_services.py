import xmlrpc
from xmlrpc import client
import datetime

class PartnerServices():
    def __init__(self,username,password):
        self.USER = username
        self.PASS = password
        self.DATA = "inimov_test_db"
        self.PORT = 8069
        self.URL = "http://localhost"
        self.URL_COMMON = "{}:{}/xmlrpc/2/common".format(self.URL,self.PORT)
        self.URL_OBJECT = "{}:{}/xmlrpc/2/object".format(self.URL,self.PORT)

    def authenticateUser(self):
        try:
            self.ODOO_COMMON = xmlrpc.client.ServerProxy(self.URL_COMMON)
            self.ODOO_OBJECT = xmlrpc.client.ServerProxy(self.URL_OBJECT)
            self.UID = self.ODOO_COMMON.authenticate(
                self.DATA,
                self.USER,
                self.PASS,{})
        except Exception as e:
            return "We encounter an Error while connecting to Odoo Server \n\n Error Message :"+str(e)
        return self.UID

    def partnerAdd(self,partnerRow):
        try:
            partner_id = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
            'res.partner', 'create',partnerRow)
        except Exception:
            return False
        return partner_id

    def getPartnerIdByEmail(self, partnerEmail):
        odoo_filter = [[("email","=", partnerEmail)]]
        try:
            partner_id = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
                'res.partner', 'search',odoo_filter)
        except Exception as e:
            print(e)
            return False
        return partner_id[0]

    def getPartnerDetailsById(self, partner_id):
        odoo_filter = [[("email","=", partner_id)]]
        try:
            partner_id = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
                'res.partner', 'read',[partner_id],{"fields":["name","id","website","phone","email","country_id"]})
        except Exception as e:
            print(e)
            return False
        return partner_id[0]

    def PartnerUpdate(self, partner_id,odoo_filter):
        try:
            update_result = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
                'res.partner', 'write',[partner_id,odoo_filter])
        except Exception as e:
            print(e)
            return False
        return update_result

    def getCountriesIds(self):
        odoo_filter = [[]]
        partner_id=None
        try:
            partner_id = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
                'res.country', 'search',odoo_filter)
        except Exception as e:
            print(e)
            return False
        if partner_id:
            try:
                country_list = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
                    'res.country', 'read',
                    [partner_id], {'fields': ['id', 'name', 'code']})
            except Exception as e:
                print(e)
                return False

        return country_list
    def partnerDelete(self, partner_id):
        delete_result = self.ODOO_OBJECT.execute_kw(self.DATA,self.UID,self.PASS,
                'res.country', 'unlink',
                    [partner_id])
        return delete_result
    