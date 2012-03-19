from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.forms import SplitDateTimeField, TextInput, MultiWidget
from django.contrib.admin import widgets as admin_widgets

from django.conf import settings

#--------------------------------------------------------------------------------

class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, *args, **kw):
        self.related_model = related_model
        return super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

    def render(self, name, value, *args, **kwargs):
        rel_to = self.related_model
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        related_url = reverse('admin:%s_%s_add' % info)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (related_url, name))
        output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))

#--------------------------------------------------------------------------------

class RelatedMultipleFieldWidgetCanAdd(widgets.SelectMultiple):

    def __init__(self, related_model, *args, **kw):
        self.related_model = related_model
        return super(RelatedMultipleFieldWidgetCanAdd, self).__init__(*args, **kw)

    def render(self, name, value, *args, **kwargs):
        rel_to = self.related_model
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        related_url = reverse('admin:%s_%s_add' % info)
        output = [ super(RelatedMultipleFieldWidgetCanAdd, self).render(
            name, value, *args, **kwargs
        ) ]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (related_url, name))
        output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))

#--------------------------------------------------------------------------------

class SplitDateTimeFormatAwareWidget(admin_widgets.AdminSplitDateTime):

    def __init__(self, *args, **kw):
        super(SplitDateTimeFormatAwareWidget, self).__init__(*args, **kw)
        self.widgets[0].format=settings.DATE_INPUT_FORMATS[0]
        self.widgets[1].widget = admin_widgets.AdminTimeWidget()
        self.widgets[1].format=settings.TIME_INPUT_FORMATS[0]

#--------------------------------------------------------------------------------

class DateFormatAwareWidget(admin_widgets.AdminDateWidget):

    def __init__(self, *args, **kw):
        super(DateFormatAwareWidget, self).__init__(*args, **kw)
        self.format=settings.DATE_INPUT_FORMATS[0]

#--------------------------------------------------------------------------------

class SplitDateTimeFieldWithClean(SplitDateTimeField):

#    def __init__(self, *args, **kw):
#        super(SplitDateTimeFieldWithClean, self).__init__(*args, **kw)
#        self.fields.append( =settings.DATE_INPUT_FORMATS[0]

#    class Media:
#        #extend = True
#        js = ('widget_util.js',)

    def render(self, name, *args, **kwargs):
        html = super(SplitDateTimeFieldWithClean, self).render(name, *args, **kwargs)
        #plus = render_to_string("form/plus.html", {'field': name})
        plus = "<label >Test:</label>"
        #print "renderrenderrenderrenderrenderrenderrenderrenderrender:  %s " % html
        return html+plus

#    def render(self, name, value, attrs=None):
#        return mark_safe(self.format_output(output))
#    def format_output(self, rendered_widgets):
#        """
#        format_output that is called when returning output. 
#        output is a list of rendered widgets html as strings
#        """
#        #print "rendered_widgets:  %s " % rendered_widgets
#        rendered_widgets.insert(0, "<label >Test:</label>")
#        return u''.join(rendered_widgets)

#class SplitDateTimeFieldWithClean(MultiWidget):

#    def __init__(self, *args, **kw):
#        widgets = (
#            SplitDateTimeField,
#            TextInput()
#        )
#        super(SplitDateTimeFieldWithClean, self).__init__(widgets, *args, **kw)

#    def decompress(self, value):
#        if value:
#            if isinstance(value, bool):
#                return ['bool', value]
#            if isinstance(value, float):
#                return ['float', value]
#            if isinstance(value, int):
#                return ['int', value]
#            if isinstance(value, basestring):
#                return ['string', value]
#            else:
#                raise Exception("Invalid type found: %s" % type(value))
#        return [None, None]

