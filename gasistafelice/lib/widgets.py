from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets

from django.conf import settings

class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, *args, **kw):
        self.related_model = related_model
        return super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)
    def render(self, name, value, *args, **kwargs):
        rel_to = self.related_model
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        related_url = reverse('admin:%s_%s_add' % info)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        # TODO: "id_" is hard-coded here. This should instead use the correct
        # API to determine the ID dynamically.
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (related_url, name))
        output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))


