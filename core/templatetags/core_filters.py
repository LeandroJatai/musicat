from compressor.utils import get_class
from django import template

from core.models import Classe


register = template.Library()


@register.filter
def objects_all_model(class_name):
    model = get_class(class_name)
    objects_all_model = model.objects.all()
    return list(objects_all_model)


@register.filter
def spaces(value):
    value = value.replace(' ', '&nbsp;')
    return value