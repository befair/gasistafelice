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
from gasistafelice.auth import DES_ADMIN
from gasistafelice.auth.models import ParamRole
from gasistafelice.auth.utils import register_parametric_role

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
    
    display_fields = (
        models.PositiveIntegerField(verbose_name=_("GAS"), name="tot_gas"),
        models.PositiveIntegerField(verbose_name=_("Gasmembers"), name="tot_gasmembers"),
        models.PositiveIntegerField(verbose_name=_("Suppliers"), name="tot_gasmembers"),
        models.PositiveIntegerField(verbose_name=_("Pacts"), name="tot_pacts"),
        models.PositiveIntegerField(verbose_name=_("Orders"), name="tot_orders"),
        models.PositiveIntegerField(verbose_name=_("Money"), name="tot_money"),
    )

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
    
    # authorization API
    
    @property
    def admins(self):
        """
        Return all users being administrators for this DES.
        """
        # retrieve 'DES administrator' parametric role for this DES
        pr = ParamRole.get_role(DES_ADMIN, des=self)
        # retrieve all Users having this role
        return pr.get_users()       
    
        
    def setup_roles(self):
        # register a new `DES_ADMIN` role for this DES
        register_parametric_role(name=DES_ADMIN, des=self)
    

    bound_resource = None

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

    #TODO placeholder domthu update limits abbreviations with resource abbreviations
    def quick_search(self, q, limits=['gn','sn','ogn','osn']):
        """Search with limit.
        @param q: search query
        @param limits: limit of search.
            * gn: GAS name
            * sn: Supplier name
            * ogn: Order GAS name
            * osn: Order Supplier name
        """

        l = []
        for i in limits:
            i = i.lower()
            if i == 'gn':
                l += self.gas_list.filter(name__icontains=q)
            if i == 'sn':
                l += self.suppliers.filter(name__icontains=q)
            elif i == 'ogn':
                l += self.orders.open().filter(pact__gas__name=q)
            elif i == 'osn':
                l += self.orders.open().filter(pact__supplier__name=q)
            else:
                pass

        ll = []
        for x in l:
            if x not in ll:
                ll.append(x)
        return ll

    @property
    def tot_gas(self):
        from gasistafelice.gas.models import GAS
        return GAS.objects.count()

    @property
    def tot_gasmembers(self):
        from gasistafelice.gas.models import GASMember
        return GASMember.objects.count()

    @property
    def tot_suppliers(self):
        from gasistafelice.supplier.models import Supplier
        return Supplier.objects.count()

    @property
    def tot_orders(self):
        from gasistafelice.gas.models import GASSupplierOrder
        return GASSupplierOrder.objects.count()

    @property
    def tot_pacts(self):
        from gasistafelice.gas.models import GASSupplierSolidalPact
        return GASSupplierSolidalPact.objects.count()

    @property
    def tot_money(self):
        # TODO improve performace: update-on-signal?
        from gasistafelice.gas.models import GASMemberOrder
        rv = 0
        for gmo in GASMemberOrder.objects.all():
            rv += gmo.ordered_price
        return rv

    #-- Resource API --#
    @property
    def ancestors(self):
        return []

    @property
    def site(self):
        return self

    @property
    def gas_list(self):
        return self.gas_set.all()

    @property
    def persons(self):
        from gasistafelice.base.models import Person
        return Person.objects.all()

    @property
    def accounts(self):
        #return Account.objects.all()
        raise NotImplementedError

    @property
    def gasmembers(self):
        from gasistafelice.gas.models.base import GASMember
        tmp = self.gas_list
        return GASMember.objects.filter(gas__in=tmp)

    @property
    def categories(self):
        from gasistafelice.supplier.models import ProductCategory
        # All categories
        return ProductCategory.objects.all()

    @property
    def pacts(self):
        """Return pacts bound to all GAS in DES"""
        from gasistafelice.gas.models.base import GASSupplierSolidalPact
        tmp = self.gas_list
        return GASSupplierSolidalPact.objects.filter(gas__in=tmp)

    @property
    def suppliers(self):
        from gasistafelice.supplier.models import Supplier
        return Supplier.objects.all()

    @property
    def orders(self):
        from gasistafelice.gas.models.order import GASSupplierOrder
        tmp = self.pacts
        return GASSupplierOrder.objects.filter(pact__in=tmp)

    @property
    def order(self):
        #Return one order for one GAS for one supplier in this des using filtering
        raise NotImplementedError

    @property
    def products(self):
        from gasistafelice.supplier.models import Product
        return Product.objects.all()

    @property
    def stocks(self):
        from gasistafelice.supplier.models import SupplierStock
        return SupplierStock.objects.all()

    @property
    def gasstocks(self):
        from gasistafelice.gas.models.order import GASSupplierStock
        return GASSupplierStock.objects.all()

    @property
    def orderable_products(self):
        from gasistafelice.gas.models.order import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.all()

    @property
    def ordered_products(self):
        from gasistafelice.gas.models.order import GASMemberOrder
        return GASMemberOrder.objects.all()

    @property
    def basket(self):
        from gasistafelice.gas.models.order import GASMemberOrder
        return GASMemberOrder.objects.filter(order__in=self.orders.open())
    
    #-------------- Authorization API ---------------#
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, context):
        # Who can create a new DES ?
        # * Only a MegaSuperUser ! ;-)
        return False # superusers skip every access-control check
    
    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit DES details ?
        # * DES administrators
        allowed_users = self.admins            
        return user in allowed_users
    
    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a DES ?
        # "DESs shouldn't die, only born" !  
        return False
            
    #---------------------------------------------------#

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
            

