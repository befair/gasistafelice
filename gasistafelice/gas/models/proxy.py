from django.db import models
from django.core.exceptions import MultipleObjectsReturned

from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier, Product, ProductCategory, ProductMU, SupplierStock, SupplierReferrer, Certification
from gasistafelice.gas.models.base import GAS, GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.models.order import GASSupplierOrder, Delivery, Withdrawal, GASSupplierOrderProduct, GASMemberOrder
from gasistafelice.des.models import DES, Siteattr
from gasistafelice.bank.models import Account, Movement

from gasistafelice.exceptions import NoSenseException
#-------------------------------------------------------------------------------

class GAS(GAS):

    class Meta:
        proxy = True

#-------------------------------------------------------------------------------

class GASMember(GASMember):

    class Meta:
        proxy = True

#-------------------------------------------------------------------------------

class DES(DES):

    class Meta:
        proxy = True

    @property
    def site(self):
        return self

    @property
    def gas_list(self):
        return self.gas_set.all()

    @property
    def accounts(self):
        #return Account.objects.all()
        raise NotImplementedError

    @property
    def gasmembers(self):
        tmp = self.gas_list
        return GASMember.objects.filter(gas__in=tmp)

    @property
    def categories(self):
        # All categories
        return ProductCategory.objects.all()

    @property
    def pacts(self):
        """Return pacts bound to all GAS in DES"""
        tmp = self.gas_list
        return GASSupplierSolidalPact.objects.filter(gas__in=tmp)

    @property
    def suppliers(self):
        tmp = self.pacts
        return Supplier.objects.filter(pk__in=[obj.supplier.pk for obj in tmp])

    @property
    def orders(self):
        tmp = self.pacts
        return GASSupplierOrder.objects.filter(pact__in=tmp)

    @property
    def order(self):
        #Return one order for one GAS for one supplier in this des using filtering
        raise NotImplementedError

    @property
    def products(self):
        return Product.objects.all()

    @property
    def stocks(self):
        return SupplierStock.objects.all()

    @property
    def gasstocks(self):
        return GASSupplierStock.objects.all()

    @property
    def orderable_products(self):
        return GASSupplierOrderProduct.objects.all()

    @property
    def ordered_products(self):
        return GASMemberOrder.objects.all()

    @property
    def basket(self):
        return GASMemberOrder.objects.filter(order__in=self.orders.open())

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

class Siteattr(Siteattr):

    class Meta:
        proxy = True

    @classmethod
    def get_site(cls):
        # Get the one and only one DES object that exists
        # FUTURE TODO: in a multi-site environment, current site can be retrieved in views
        # https://docs.djangoproject.com/en/1.3/ref/contrib/sites/
        rv = DES.objects.order_by('id').all()[0]
        return rv
    
#-------------------------------------------------------------------------------

class Person(Person):

    class Meta:
        proxy = True

    @property
    def persons(self):
        return Person.objects.filter(pk=self.pk)

    @property
    def person(self):
        return self

    @property
    def gasmembers(self):
        return self.gasmember_set.all()

    @property
    def gasmember(self):
        """GAS member bound to this person.

        @raises DoesNotExist if person is not a GASMember
        @raises MultipleObjectsReturned if more than one GAS found
        """
        return GASMember.objects.get(person=self)

    @property
    def gas_list(self):
        gas_pks = [obj.gas.pk for obj in self.gasmembers]
        return GAS.objects.filter(pk__in=gas_pks)

    @property
    def gas(self):
        """GAS bound to this person.

        @raises DoesNotExist if person is not a GASMember
        @raises MultipleObjectsReturned if more than one GAS found
        """
        return self.gasmember.gas

    @property
    def suppliers(self):
        rv = Supplier.objects.none()
        for gas in self.gas_list:
            rv |= gas.suppliers
        return rv

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(gas__in=self.gas_list)

    @property
    def order(self):
        """This is not needed because a Person which is a GAS Member will have many orders"""
        raise NotImplementedError

#-------------------------------------------------------------------------------

class Supplier(Supplier):

    class Meta:
        proxy = True

#-------------------------------------------------------------------------------

class Product(Product):

    class Meta:
        proxy = True

    @property
    def products(self):
        return Product.objects.filter(pk=self.pk)

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def categories(self):
        return ProductCategory.objects.filter(product_set__in=[self])

    @property
    def suppliers(self):
        return Supplier.objects.filter(stock_set__in=self.stocks)

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(stock_set__in=self.stocks)

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

class GASSupplierOrder(GASSupplierOrder):

    class Meta:
        proxy = True

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(pk=self.pk)

    @property
    def order(self):
        return self

    @property
    def gas(self):
        return self.pact.gas

    @property
    def supplier(self):
        return self.pact.supplier

#TODO: des, person, gasmember, product, category

#-------------------------------------------------------------------------------

class ProductCategory(ProductCategory):

    class Meta:
        proxy = True

    @property
    def categories(self):
        return ProductCategory.objects.filter(pk=self.pk)

#TODO: des, gas, supplier, product, order

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

