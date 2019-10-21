from django import template

register = template.Library()


@register.simple_tag
def gen_role_url(request, rid):

    params = request.GET.copy()
    params._mutable = True
    params['rid'] = rid
    return params.urlencode()