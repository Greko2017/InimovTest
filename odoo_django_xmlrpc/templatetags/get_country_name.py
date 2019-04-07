from django import template
import datetime
register = template.Library()
 
@register.filter
def get_country_name(country_datas):
    country_dic={}
    country_dic = {"id":country_datas[0],"name":country_datas[1]}
    return country_dic['name']