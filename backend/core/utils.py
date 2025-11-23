
def is_htmx_request(request):
    is_htmx = getattr(request, 'htmx', False)
    if is_htmx:
        return True
    else:
        return False
