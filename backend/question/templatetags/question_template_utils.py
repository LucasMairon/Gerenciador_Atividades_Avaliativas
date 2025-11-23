from django import template

register = template.Library()


@register.simple_tag()
def decimal_to_letter(index):
    ascii_value = 64 + index

    return chr(ascii_value)
