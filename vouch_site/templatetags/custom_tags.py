from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    if isinstance(d, dict):
        return d.get(key)
    return None


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})
