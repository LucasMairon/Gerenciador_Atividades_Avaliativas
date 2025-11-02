from django import template

from django.http import HttpRequest

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active_app(context, url_name):
    request: HttpRequest = context.get('request')

    if not request:
        return ""
    view_url_name = request.resolver_match.view_name

    if view_url_name.startswith(url_name):
        return 'active'
    else:
        return ""
