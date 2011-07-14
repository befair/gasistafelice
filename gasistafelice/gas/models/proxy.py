from django.db import models

from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier, Product, ProductCategory
from gasistafelice.gas.models import GAS, GASMember, GASSupplierOrder, GASSupplierSolidalPact, Delivery, Withdrawal
from gasistafelice.des.models import DES
from gasistafelice.bank.models import Account

#-------------------------------------------------------------------------------

class GAS(GAS):

    class Meta:
        proxy = True

    @property
    def orders(self):
        """Return orders bound to resource"""
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def pacts(self):
        """Return pacts bound to a GAS"""
        #return self.pacts_set.all()
        return self.pacts_gas_set.all()

    @property
    def solidal_pacts(self):
        """Return pacts bound to a GAS"""
        #return GASSupplierSolidalPact.objects.filter(gas=self)
        return GASSupplierSolidalPact.objects.all()

    @property
    def accounts(self):
        #return Account.objects.filter(pk=self.account.pk | pk=self.liquidity.pk).order_by('balance')
        result = []
        result.append(Account.objects.get(pk=self.account.pk))
        result.append(Account.objects.get(pk=self.liquidity.pk))
        return result

    @property
    def gasmembers(self):
        return GASMember.objects.filter(gas=self)

    @property
    def suppliers(self):
        p = GASSupplierSolidalPact.objects.filter(gas=self)
        return Supplier.objects.filter(pk__in=[obj.supplier.pk for obj in p])
        #return Supplier.objects.all()

    def categories(self):
        #TODO All disctinct categories for all suppliers with solidal pact for associated list of products
        return ProductCategory.objects.all()

#-------------------------------------------------------------------------------

class GASMember(GASMember):

    class Meta:
        proxy = True

    @property
    def des(self):
        # A GAS member belongs to the DES its GAS belongs to.
        return self.gas.des
    
    @property
    def pacts(self):
        # A GAS member is interested primarily in those pacts (`SupplierSolidalPact` instances) subscribed by its GAS
        return self.gas.pacts 
    
    @property
    def suppliers(self):
        # A GAS member is interested primarily in those suppliers dealing with its GAS
        return self.gas.suppliers
    
    @property
    def orders(self):
        # A GAS member is interested primarily in those suppliers orders to which he/she can submit orders
        return self.gas.orders
    
    @property
    def deliveries(self):
        # A GAS member is interested primarily in delivery appointments scheduled for its GAS
        return self.gas.deliveries
    
    @property
    def withdrawals(self):
        # A GAS member is interested primarily in withdrawal appointments scheduled for its GAS
        return self.gas.withdrawals
    
    @property
    def products(self):
        # A GAS member is interested primarily in those products he/she can order
        return self.gas.products
    

    
#-------------------------------------------------------------------------------

class DES(DES):

    class Meta:
        proxy = True

    @property
    def site(self):
        return self

    @property
    def gas_list(self):
        return GAS.objects.all()
        #TODO: enable the following when database is updated with des attribute for GAS
        # return self.gas_set.all()

    #TODO placeholder domthu define Resource API
    #TODO placeholder domthu define other properties for all resources in RESOURCE_LIST
    @property
    def gas_list(self):
        return GAS.objects.all()
        #TODO: enable the following when database is updated with des attribute for GAS
        # return self.gas_set.all()

    # Resource API
    @property
    def accounts(self):
        return Account.objects.all()

    # Resource API
    @property
    def gasmembers(self):
        if hasattr(self, 'isfiltered') and self.isfiltered:
            return GASMember.objects.filter(pk__in=[obj.pk for obj in self.all_gasmembers])
        return GASMember.objects.all()

    # Resource API
    @property
    def gasmembers(self):
        if hasattr(self, 'isfiltered') and self.isfiltered:
            return GASMember.objects.filter(pk__in=[obj.pk for obj in self.all_gasmembers])
        return GASMember.objects.all()

    # Resource API
    def categories(self):
        # All categories 
        return ProductCategory.objects.all()

    # Resource API
    @property
    def suppliers(self):
        return Supplier.objects.all()

    @property
    def pacts(self):
        """Return pacts bound to all GAS in DES"""
        return self.pacts_gas_set.all()

    @property
    def solidal_pacts(self):
        """Return pacts bound to all GAS in DES"""
        #g = self.gas_list
        #return GASSupplierSolidalPact.objects.filter(gas__in=g)
        return GASSupplierSolidalPact.objects.all()

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

#-------------------------------------------------------------------------------

class Account(Account):

    class Meta:
        proxy = True

    @property
    def accounts(self):
        return self

#-------------------------------------------------------------------------------


