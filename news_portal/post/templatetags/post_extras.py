from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="censor")
@stringfilter
def censor(value, arg):
    """Заменяет в строке исключительное слово на *."""
    return value.replace(arg, "*")
