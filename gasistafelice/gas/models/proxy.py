from django.db import models
from django.core.exceptions import MultipleObjectsReturned

from gasistafelice.base.models import Person
from gasistafelice.supplier.models import Supplier, Product, ProductCategory, ProductMU, SupplierStock, SupplierReferrer, Certification
from gasistafelice.gas.models.base import GAS, GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.models.order import GASSupplierOrder, Delivery, Withdrawal, GASSupplierOrderProduct, GASMemberOrder
from gasistafelice.des.models import DES, Siteattr

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


class Siteattr(Siteattr):

    class Meta:
        proxy = True

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


#TODO: des, gas, gasmember, supplier

