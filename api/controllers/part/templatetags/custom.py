from django import template

register = template.Library()


@register.filter(name="to_slash")
def to_slash(value):
    return value.__str__().replace("->", "/")


@register.filter(name="to_list")
def to_list(value, splt):
    return value.__str__().split(splt)
