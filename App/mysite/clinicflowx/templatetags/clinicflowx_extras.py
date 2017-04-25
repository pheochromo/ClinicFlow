from django import template

register = template.Library()

@register.filter
def filterPreReqs(value):
    return ",".join(value)
