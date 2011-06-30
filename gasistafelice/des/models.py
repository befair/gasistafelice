# Copyright (C) 2011 REES Marche <http://www.reesmarche.org>
# taken from SANET - Laboratori Guglielmo Marconi S.p.A. <http://www.labs.it>
#
# This file is part of GASISTA FELICE
# GASISTA FELICE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License
#
# GASISTA FELICE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with GASISTA FELICE. If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.comments.models import Comment

from django.contrib.sites.models import Site

from gasistafelice.lib import ClassProperty
from gasistafelice.base.models import Resource

import time

#------------------------------------------------------------------------------
# Basic DES object: configuration registry

class DES(Site, Resource):
    """Facade for Siteattr object. It's an orthogonal representation for it.
    It proxies get attribute operations. 
    It is a Model instance since there are foreign key for it (i.e. comments)

    TODO: cache attributes in order to avoid database operations.
    (stub for validity already done)

    >>> Siteattr.get_attribute_or_empty('name') == DES.name
    True
    """

    cfg_time = models.PositiveIntegerField()
    
    display_fields = ()

    class Meta:
        verbose_name = _("site")
        verbose_name_plural = _("sites")

    @ClassProperty
    @classmethod
    def resource_type(cls):
        return "site" #avoid to change custom js and html with "des"

    def __init__(self, *args, **kw):
        super(DES, self).__init__(*args, **kw)

        self.isfiltered = False

        # Set an attribute for each Siteattr var name
        for attr in Siteattr.known_names_types:
            setattr(self, attr, Siteattr.get_attribute_or_empty(attr))
        self.cfg_time = Siteattr.get_site_config_timestamp()
        
    @property
    def icon(self):
        if hasattr(self, 'icon_id'):
            return Icon.objects.get(id=int(self.icon_id))
        else:
            return Icon.objects.get(name='site')
            
    def __unicode__(self):
        return self.name

    bound_resource = None

    @property
    def gas_list(self):
        return GAS.objects.all()
        #TODO: enable the following when database is updated with des attribute for GAS
        return self.gas_set.all()

    #TODO placeholder domthu define other properties for all resources in RESOURCE_LIST

    @property
    def gasmembers(self):
        if hasattr(self, 'isfiltered') and self.isfiltered:
            return GASMember.objects.filter(pk__in=[obj.pk for obj in self.all_gasmembers])
        return GASMember.objects.all()

    #TODO placeholder domthu update limits abbreviations with resource abbreviations
    def quick_search(self, name, limits=['cn','cd','nn','nd','in','id','ii','tp','tt','td','mp','mt','md']):

        l = []
        for i in limits:
            if i.lower() == 'cn':
                l += self.containers.filter(name__icontains=name)
            elif i.lower() == 'cd':
                l += self.containers.filter(descr__icontains=name)
            elif i.lower() == 'nn':
                l += self.nodes.filter(name__icontains=name)
            elif i.lower() == 'nd':
                l += self.nodes.filter(descr__icontains=name)
            elif i.lower() == 'in':
                l += self.ifaces.filter(name__icontains=name)
            elif i.lower() == 'id':
                l += self.ifaces.filter(descr__icontains=name)
            elif i.lower() == 'ii':
                l += self.ifaces.filter(instance__icontains=name)
            elif i.lower() == 'tp':
                l += self.targets.filter(path__icontains=name)
            elif i.lower() == 'tt':
                l += self.targets.filter(title__icontains=name)
            elif i.lower() == 'td':
                l += self.targets.filter(descr__icontains=name)
            elif i.lower() == 'mp':
                l += self.measures.filter(path__icontains=name)
            elif i.lower() == 'mt':
                l += self.measures.filter(title__icontains=name)
            elif i.lower() == 'md':
                l += self.measures.filter(descr__icontains=name)
            else:
                pass
        ll = []
        for x in l:
            if x not in ll:
                ll.append(x)
        return ll

    def is_configured(self):
        name = Siteattr.get_attribute_or_none('name')
        if name == None:
            return False
        
        return True

    def filter(self, user):
        """Filter results by user. In our site (DES) there's nothing to hide to users"""
        #DISABLED we do not need this
        #TODO placeholder fero: check if it could be useful
        return self

    @property
    def allnotes(self):

        # The view on the site is filtered by user.
        # Deeply select notes only from visible root_containers
        if  hasattr(self, 'isfiltered') and self.isfiltered:
            
            notes = [ n for n in super(DES, self).allnotes ]
            
            if recursive_queries:
                
                # Notes of all root containers
                for rc in self.trees:
                    notes += rc.notes
        
                # Recursive search in root containers
                selected_resources = ' union '.join([ 'SELECT * FROM container_subresources(%s)'%(rc.id) for rc in self.trees ])

                if selected_resources:
                    query_str = """
                    SELECT n.*
                      FROM (SELECT distinct * FROM (%s) s_r)  AS r
                           INNER JOIN django_content_type AS ct ON (r.model = ct.model)
                           INNER JOIN django_comments     AS n ON (ct.id = n.content_type_id) AND (r.pk::text = n.object_pk)
                     WHERE n.is_removed = false
                    """ % (selected_resources)
                    # ORDER BY n.submit_date DESC;
                    
                    notes += [ n for n in Comment.objects.raw(query_str) ]
                
            notes = sorted(notes, key=(lambda x: x.submit_date), reverse=True)
                
            return notes
        else:
            return Comment.objects.filter(is_removed=False).order_by('-submit_date').all()

class Siteattr(models.Model):

    name = models.CharField(verbose_name=_('name'), max_length=63, null=False, blank=False, db_index=True, unique=True)
    value = models.TextField(verbose_name=_('value'), null=False, blank=True, db_index=False, unique=False)
    atype = models.CharField(verbose_name=_('type'), max_length=63, null=False, blank=False, db_index=False, unique=False)
    descr = models.CharField(max_length=255, blank=True, default='', db_index=False)

    # Reserved attribute (not updatable with Siteattr.set_attribute)
    SITE_CONFIG_TIME_ATTR = 'site_config_timestamp'

    known_names_types = {
        'name':'varchar',
        'icon_id':'integer',
        'descr':'varchar',
        'details':'text',
        'banner':'varchar',
        #TODO placeholder fero: db schema versioning needed? 'schema':'integer',
    }

    known_names_def_descriptions = {
         'name'             : 'Site name'
        ,'icon_id'          : 'Site icon'
        ,'descr'            : 'Site description'
        ,'details'          : 'Site HTML details'
        ,'banner'           : 'Site CLI banner'
    }

    class Meta:
        verbose_name = _("environment variable")
        verbose_name_plural = _("environment variables")
        ordering = ['name']

    def __unicode__(self):
        return "%s[%s]" % (self.name, self.atype)

    @classmethod
    def get_site(cls):
        # Get the one and only one DES object that exists
        # FUTURE TODO: in a multi-site environment, current site can be retrieved in views
        # https://docs.djangoproject.com/en/1.3/ref/contrib/sites/
        rv = DES.objects.order_by('id').all()[0]
        return rv
    
    @staticmethod
    def set_attribute(name, value, descr):
        if not Siteattr.known_names_types.has_key(name):
            raise ValueError, 'Unknown Siteattr %s' % name
        if (Siteattr.known_names_types[name] == 'varchar') and len(value) > 255:
            raise ValueError, 'Attempting to set a value too long for Siteattr %s (max 255)' % name

        v=Siteattr.objects.filter(name=name)
        if len(v) == 0:
            Siteattr(name=name, value=value, atype=Siteattr.known_names_types[name], descr=descr).save()
        else:
            v[0].value=value
            v[0].save()

    @staticmethod
    def get_attribute_or_none(name):
        if not Siteattr.known_names_types.has_key(name):
            raise ValueError, 'Unknown Siteattr %s' % name
        t=None
        try:
            t=Siteattr.objects.filter(name=name)[0].value
        except:
            pass
        return t

    @staticmethod
    def get_attribute_or_empty(name):
        t=Siteattr.get_attribute_or_none(name)
        if t != None:
            return t
        if Siteattr.known_names_types[name] == 'varchar':
            return ''
        return 0

    @staticmethod
    def get_site_config_timestamp():
        t = 0
        try:
            t=Siteattr.objects.filter(name=Siteattr.SITE_CONFIG_TIME_ATTR)[0].value
        except:
            pass
        return t

    def save(self, *args, **kwargs):
        super(Siteattr, self).save(*args, **kwargs)

        if self.name != Siteattr.SITE_CONFIG_TIME_ATTR:
            # Update site config time
            cfg_time, created = Siteattr.objects.get_or_create(name=Siteattr.SITE_CONFIG_TIME_ATTR)
            cfg_time.value = int(time.time())
            if created:
                cfg_time.atype='timestamp'
                cfg_time.descr='Last site modification timestamp'
            cfg_time.save()
            

