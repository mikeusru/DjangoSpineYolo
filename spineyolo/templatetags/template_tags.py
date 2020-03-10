from django import template

from spineyolo.models import SpineData

register = template.Library()


@register.simple_tag
def get_obj(pk, *attrs):
    try:
        """ Get object based on any number of attributes
            (attributes need to be children of one another) """
        attrs = list(attrs)
        obj = getattr(SpineData.objects.get(pk=int(pk)), attrs.pop(0))
        for attr in attrs:
            obj = getattr(obj, attr, "")
    except ValueError:
        obj = ""
    return obj
