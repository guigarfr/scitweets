from django import template

register = template.Library()

@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)

class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    from django.views.i18n import set_language
    from django.core.urlresolvers import resolve, reverse
    from django.utils.translation import activate, get_language
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """

    path = context['request'].path
    url = path
    cur_language = get_language()

    context['request'].POST = context['request'].POST.copy()
    context['request'].POST['language'] = lang
    context['request'].POST['next'] = path

    try:
        print "Change language to ", lang
        set_language(context['request'])
    except Exception, e:
        pass
    finally:
        print "Error!!"
    return "%s" % url
