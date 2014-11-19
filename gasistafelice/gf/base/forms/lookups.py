from django.utils.html import escape

from ajax_select import LookupChannel

from gf.base.models import Place, Person

class PlaceLookup(LookupChannel):

    model = Place

    def get_query(self,q,request):
        qs = Place.objects.filter(name__icontains=q)
        qs |= Place.objects.filter(address__icontains=q)
        qs |= Place.objects.filter(city__icontains=q)
        return qs.order_by('city','name')[:10]

#    def get_result(self,obj):
#        log.debug(obj,"BBBBBB")
#        return unicode(obj)
        
    def format_match(self,obj):
        return self.format_item_display(obj)

#    def format_item_display(self,obj):
#        
##        return u"%s<div><i>%s</i></div>" % (escape(obj.city),escape(obj.name))
#        values = (escape(obj.name),escape(obj.zipcode),escape(obj.city))
#        format = u"%s - %s %s"
#        if len(obj.province) > 0:
#            values = values + (escape(obj.province),) # the final , forces tuple concatenation -FS
#            format += " (%s)"
#            
#        #log.debug("values=", values)    
#            
#        return format % values 

    def can_add(self,user,model):
        """ 
        Customize can_add by allowing anybody to add a Group.
        the superclass implementation uses django's permissions system to check.
        only those allowed to add will be offered a [+ add] popup link
        """
        return True

class PersonLookup(LookupChannel):

    model = Person

    def get_query(self,q,request):
        qs = Person.objects.filter(name__icontains=q)
        qs |= Person.objects.filter(surname__icontains=q)
        qs |= Person.objects.filter(display_name__icontains=q)
        return qs.order_by('surname','name')[:10]

#    def get_result(self,obj):
#        log.debug(obj,"BBBBBB")
#        return unicode(obj)
        
    def format_match(self,obj):
        return self.format_item_display(obj)

    def format_item_display(self,obj):
        try:
            url = obj.avatar.url
        except ValueError as e:
            url = ""
        
        return u'<img src="%s" /> %s' % (url, escape(unicode(obj)))

    def can_add(self,user,model):
        """ 
        Customize can_add by allowing anybody to add a Group.
        the superclass implementation uses django's permissions system to check.
        only those allowed to add will be offered a [+ add] popup link
        """
        return True
