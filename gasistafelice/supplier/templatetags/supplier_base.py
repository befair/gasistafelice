
from django import template
from django.utils.translation import ugettext as _


register = template.Library()

@register.simple_tag
def render_stock_versions(versions):
    rendering = u""
    for id, version in enumerate(reversed(versions)):
        rendering += u"modificato in data %s dall'utente %s: (%s) - prezzo (%s)" % (
            '{0:%d-%M-%Y alle %H:%M}'.format(version.revision.date_created),
            version.revision.user.person if version.revision.user else version.revision.user,
            version, version.object_version.object.price
        )
        if id < (len(versions) - 1):
            rendering += " ----> "

    return rendering

