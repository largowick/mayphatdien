from django import template
from mayphat.models import Infor

register = template.Library()


@register.simple_tag
def get_addressee():
    infor = Infor.objects.all()
    for x in infor:
        infor = x
    return infor
