from django.db import models

from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier, Product, ProductCategory, ProductMU, SupplierStock, SupplierReferrer, Certification
from gasistafelice.gas.models.base import GAS, GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.models.order import GASSupplierOrder, Delivery, Withdrawal, GASSupplierOrderProduct, GASMemberOrder
from gasistafelice.des.models import DES
from gasistafelice.bank.models import Account, Movement

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
        return self.pacts_set.all()
        
    @property
    def suppliers(self):
        """Return suppliers bound to a GAS"""
        return self.supplier_set.all()
        
    @property
    def accounts(self):
        #return (Account.objects.filter(pk=self.account.pk) | Account.objects.filter(pk=self.liquidity.pk)).order_by('balance')
        raise NotImplementedError

    @property
    def gasmembers(self):
        return GASMember.objects.filter(gas=self)

    def categories(self):
        #TODO All disctinct categories for all suppliers with solidal pact for associated list of products
        raise NotImplementedError
        #TODO return ProductCategory.objects.all()

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

    @property
    def suppliers(self):
        """Return suppliers bound to the DES"""
        return Supplier.objects.all()

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
        #return Account.objects.all()
        raise NotImplementedError

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
        return self.pacts_set.all()
        #g = self.gas_list
        #return GASSupplierSolidalPact.objects.filter(gas__in=g)

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

class Person(Person):

    class Meta:
        proxy = True

    @property
    def persons(self):
        return Person.objects.filter(pk=self.pk)

#-------------------------------------------------------------------------------

class Account(Account):
    #TODO

    class Meta:
        proxy = True

    @property
    def accounts(self):
        return Account.objects.filter(pk=self.pk)

    @property
    def transacts(self):
        #return Movement.objects.filter(account=self)
        raise NotImplementedError

#TODO: des, gas, gasmember, supplier

class Movement(Movement):
    #TODO

    class Meta:
        proxy = True

    @property
    def transacts(self):
        return Movement.objects.filter(pk=self.pk)

#TODO: des, gas, gasmember, supplier, account

#-------------------------------------------------------------------------------

class Supplier(Supplier):

    class Meta:
        proxy = True

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.pk)

#TODO: des, gas, referrers, order, categories, unit measures

#-------------------------------------------------------------------------------

class Product(Product):

    class Meta:
        proxy = True

    @property
    def products(self):
        return Product.objects.filter(pk=self.pk)

#TODO: order, categories, unit measures, supplier

#-------------------------------------------------------------------------------

class SupplierReferrer(SupplierReferrer):

    class Meta:
        proxy = True

    @property
    def referrers(self):
        return SupplierReferrer.objects.filter(pk=self.pk)

#TODO: des, gas, supplier, person, gasmember

#-------------------------------------------------------------------------------

class ProductCategory(ProductCategory):

    class Meta:
        proxy = True

    @property
    def categories(self):
        return ProductCategory.objects.filter(pk=self.pk)

#TODO: des, gas, supplier, product, order

#-------------------------------------------------------------------------------

class ProductMU(ProductMU):

    class Meta:
        proxy = True

    @property
    def units(self):
        return ProductMU.objects.filter(pk=self.pk)

#TODO: des, gas, supplier, product, order

#-------------------------------------------------------------------------------

class Certification(Certification):

    class Meta:
        proxy = True

    @property
    def certs(self):
        return Certification.objects.filter(pk=self.pk)

    @property
    def cert(self):
        return self

#TODO: des, gas, supplier, person, gasmember

#-------------------------------------------------------------------------------

class SupplierStock(SupplierStock):

    class Meta:
        proxy = True

    @property
    def stocks(self):
        return SupplierStock.objects.filter(pk=self.pk)

    @property
    def stock(self):
        return self

#TODO: des, gas, supplier, product

#-------------------------------------------------------------------------------

class GASSupplierStock(GASSupplierStock):

    class Meta:
        proxy = True

    @property
    def gasstocks(self):
        return GASSupplierStock.objects.filter(pk=self.pk)

    @property
    def gasstock(self):
        return self

#TODO: des, gas, supplier, product, product2

#-------------------------------------------------------------------------------

class GASSupplierOrderProduct(GASSupplierOrderProduct):

    class Meta:
        proxy = True

    @property
    def stocks_in_order(self):
        return GASSupplierOrderProduct.objects.filter(pk=self.pk)

    @property
    def stock_in_order(self):
        return self

#TODO: des, gas, supplier, person, gasmember

#-------------------------------------------------------------------------------

class GASSupplierOrder(GASSupplierOrder):

    class Meta:
        proxy = True

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(pk=self.pk)

    @property
    def order(self):
        return self

#TODO: des, gas, supplier, person, gasmember, product, category

#-------------------------------------------------------------------------------

class GASMemberOrder(GASMemberOrder):

    class Meta:
        proxy = True

    @property
    def baskets(self):
        return GASMemberOrder.objects.filter(pk=self.pk)

    @property
    def basket(self):
        return self

#TODO: des, gas, supplier, person, gasmember, product, category, order

