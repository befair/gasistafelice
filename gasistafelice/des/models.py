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
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from lib import ClassProperty
from app_base.models import PermissionResource, Person
from app_base.utils import get_resource_icon_path
from consts import DES_ADMIN, NONDES_NAME, NONDES_SURNAME
from flexi_auth.models import ParamRole
from flexi_auth.utils import register_parametric_role

import time

#------------------------------------------------------------------------------
# Basic DES object: configuration registry

class DES(Site, PermissionResource):
    """Facade for Siteattr object. It's an orthogonal representation for it.
    It proxies get attribute operations. 
    It is a Model instance since there are foreign key for it (i.e. comments)

    TODO: cache attributes in order to avoid database operations.
    (stub for validity already done)

    #NOTE: doctest fail. Have to use initial_data.json fixture on this
    >> d = Siteattr.get_site()
    >> Siteattr.get_attribute_or_empty('name') == d.name
    True
    """

    cfg_time = models.PositiveIntegerField()
    logo = models.ImageField(upload_to=get_resource_icon_path, null=True, blank=True)
    info_people_set = models.ManyToManyField(Person, null=True, blank=True)
    
    display_fields = (
        models.PositiveIntegerField(verbose_name=_("GAS"), name="tot_gas"),
        models.PositiveIntegerField(verbose_name=_("Gasmembers"), name="tot_gasmembers"),
        models.PositiveIntegerField(verbose_name=_("Suppliers"), name="tot_suppliers"),
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
        
    def __unicode__(self):
        return self.name
    
    @property
    def icon(self):
        return self.logo or super(DES, self).icon

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
    
    @classmethod
    def admins_all(cls):
        """
        Return all users being administrators for **any** DES.
        """
        #FIXME: use a descriptor to merge this functionality with that of ``DES.admins()``
        des_admins_all = set()
        for des in cls.objects.all():
            des_admins_all = des_admins_all | des.admins
        return des_admins_all               
    
    @property
    def referrers(self):
        return self.admins

    @property
    def gas_tech_referrers(self):
        rv = User.objects.none()
        for g in self.gas_list:
            rv |= g.tech_referrers
        return rv

    @property
    def gas_supplier_referrers(self):
        rv = User.objects.none()
        for g in self.gas_list:
            rv |= g.supplier_referrers
        return rv

    @property
    def gas_cash_referrers(self):
        rv = User.objects.none()
        for g in self.gas_list:
            rv |= g.cash_referrers
        return rv

    @property
    def supplier_referrers_people(self):
        prs = Person.objects.none()
        for g in self.gas_list:
            prs |= g.supplier_referrers_people
        return prs

    @property
    def info_people(self):
        return self.info_people_set.all()
        
    def setup_roles(self):
        # register a new ``DES_ADMIN`` role for this DES
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

    def quick_search(self, q, limits=['ogn','osn','gn','sn','pn','ps']):
        """Search with limit.
        @param q: search query
        @param limits: limit of search.
            * gn: GAS name
            * sn: Supplier name
            * ogn: Order GAS name
            * osn: Order Supplier name
            * pn: Person name
            * ps: Person surname
        """

        l = []
        for i in limits:
            i = i.lower()
            if i == 'ogn':
                l += self.orders.open().filter(pact__gas__name__icontains=q)
            elif i == 'osn':
                l += self.orders.open().filter(pact__supplier__name__icontains=q)
            elif i == 'gn':
                l += self.gas_list.filter(name__icontains=q)
            elif i == 'sn':
                l += self.suppliers.filter(name__icontains=q)
            elif i == 'pn':
                l += self.persons.filter(name__icontains=q)
            elif i == 'ps':
                l += self.persons.filter(name__icontains=q)
            else:
                pass

        ll = []
        for x in l:
            if x not in ll:
                ll.append(x)
        return ll

    @property
    def tot_gas(self):
        from app_gas.models import GAS
        return GAS.objects.count()

    @property
    def tot_gasmembers(self):
        from app_gas.models import GASMember
        return GASMember.objects.count()

    @property
    def tot_suppliers(self):
        from app_supplier.models import Supplier
        return Supplier.objects.count()

    @property
    def tot_orders(self):
        from app_gas.models import GASSupplierOrder
        return GASSupplierOrder.objects.count()

    @property
    def tot_pacts(self):
        from app_gas.models import GASSupplierSolidalPact
        return GASSupplierSolidalPact.objects.count()

    @property
    def tot_money(self):
        # TODO improve performace: update-on-signal?
        from app_gas.models import GASMemberOrder
        rv = 0
        for gmo in GASMemberOrder.objects.all():
            rv += gmo.ordered_price
        return rv

    #-- Resource API --#
    @property
    def ancestors(self):
        return []

    @property
    def des(self):
        return self

    @property
    def gas_list(self):
        return self.gas_set.all()

    @property
    def gas(self):
        #Use in OpenOrderForm
        #TODO: if none the form must retrieve the gas related user logged in. What happend if superuser is the logged in?
        return None

    @property
    def persons(self):
        return Person.objects.all()

    @property
    def gasmembers(self):
        from app_gas.models.base import GASMember
        tmp = self.gas_list
        return GASMember.objects.filter(gas__in=tmp)

    @property
    def categories(self):
        from app_supplier.models import ProductCategory
        # All categories
        return ProductCategory.objects.all()

    @property
    def pacts(self):
        """Return pacts bound to all GAS in DES"""
        from app_gas.models.base import GASSupplierSolidalPact
        tmp = self.gas_list
        return GASSupplierSolidalPact.objects.filter(gas__in=tmp).order_by('gas', 'supplier')

    @property
    def suppliers(self):
        from app_supplier.models import Supplier
        return Supplier.objects.all()

    @property
    def orders(self):
        from app_gas.models.order import GASSupplierOrder
        tmp = self.pacts
        return GASSupplierOrder.objects.filter(pact__in=tmp)

    @property
    def order(self):
        #Return one order for one GAS for one supplier in this des using filtering
        raise NotImplementedError

    @property
    def products(self):
        from app_supplier.models import Product
        return Product.objects.all()

    @property
    def stocks(self):
        from app_supplier.models import SupplierStock
        return SupplierStock.objects.all()

    @property
    def gasstocks(self):
        from app_gas.models.order import GASSupplierStock
        return GASSupplierStock.objects.all()

    @property
    def orderable_products(self):
        from app_gas.models.order import GASSupplierOrderProduct
        return GASSupplierOrderProduct.objects.all()

    @property
    def ordered_products(self):
        from app_gas.models.order import GASMemberOrder
        return GASMemberOrder.objects.all()

    @property
    def basket(self):
        from app_gas.models.order import GASMemberOrder
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

    #--------------------------#


    @property
    def economic_movements(self):
        """Return accounting LedgerEntry instances."""
        from simple_accounting.models import LedgerEntry
        all_des_trx = LedgerEntry.objects.none()   #set()
        for gas in self.gas_list:
            all_des_trx |= gas.economic_movements
        for sup in self.suppliers:
            all_des_trx |= sup.economic_movements
        return all_des_trx

    @property
    def balance(self):
        """
        return all accounts for the accounting system
        
        compose by
            - GAS
            - Supplier
            - GASMembers
        """
        #FIXME: performance time not good. In debug time 22 seconds
        acc_tot = 0
        for gm in self.gasmembers:
            acc_tot += gm.balance
        for g in self.gas_list:
            acc_tot += g.balance
        for sup in self.suppliers:
            acc_tot += sup.balance
        return acc_tot

    @property
    def accounting(self):
        """
        return a Person Account.

        The NonDES person is a fictitious one that symbolize the Out Of Network accounting
        It permit to count money transfert between (entering or escaping) the DES and the market
        """
        try:
            nondes = Person.objects.get(
                name__exact=NONDES_NAME,
                surname__exact=NONDES_SURNAME
            )
        except Person.DoesNotExist:
            #Create accounting system for a NonDES in the DES accounting system

            #Possibility 1: Set DES as subject (@economic_subject) and create Accounting proxy
#            des.subject.init_accounting_system()
#            system = des.accounting.system
#            system.add_account(parent_path='/', name='cash', kind=account_type.asset)

            #Possibility 2 (LF): Create fictitious person and use it as NonDES account

            #Create the fictitious person account without address and user
            nondes = Person(name = NONDES_NAME, surname = NONDES_SURNAME)
            nondes.save()

        return nondes.accounting


#------------------------------------------------------------------------------


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
            

