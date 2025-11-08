from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def add_param_to_url(context, **kwargs):
    query_params = context['request'].GET.copy()

    for key, value in kwargs.items():
        query_params[key] = value

    return query_params.urlencode()


@register.simple_tag()
def get_message_icon(tag):
    if tag == 'success':
        return "bi bi-check-circle-fill"
    elif tag == 'danger':
        return "bi bi-exclamation-triangle-fill"
