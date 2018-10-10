from __future__ import division

from django import template

register = template.Library()

@register.filter
def clean_alert(alert):
    alert_list = alert.split('*')
    if len(alert_list)>0:
        return alert_list[-1].replace('emp id','CUID')
    else:
        return ''

