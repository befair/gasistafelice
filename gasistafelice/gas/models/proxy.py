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

    @property
    def gas(self):
        return self

    @property
    def orders(self):
        """Return orders bound to resource"""
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def order(self):
        raise NoSenseException("calling gas.order is a no-sense. GAS is related to more than one order")

    @property
    def deliveries(self):
        # The GAS deliveries appointments take from orders. Do distinct operation. 
        rv = Delivery.objects.none()
        for obj in self.orders:
            if obj.delivery: 
                rv |= obj.delivery
        return rv

    @property
    def delivery(self):
        raise NoSenseException("calling gas.delivery is a no-sense. GAS is related to more than one delivery")

    @property
    def withdrawals(self):
        # The GAS withdrawal appointments. Do distinct operation.
        rv = Withdrawal.objects.none()
        for obj in self.orders:
            if obj.withdrawal: 
                rv |= obj.withdrawal
        return rv

    @property
    def withdrawal(self):
        raise NoSenseException("calling gas.withdrawal is a no-sense. GAS is related to more than one withdrawal")

    @property
    def pacts(self):
        # Return pacts bound to a GAS
        return self.pact_set.all()

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
        return self.gasmember_set.all()

    @property
    def stocks(self):
        return SupplierStock.objects.filter(supplier__in=self.suppliers)

    @property
    def products(self):
        return Product.objects.filter(pk__in=[obj.product.pk for obj in self.stocks])

    @property
    def categories(self):
        #TODO All disctinct categories for all suppliers with solidal pact with the gas
        #distinct(pk__in=[obj.category.pk for obj in self.Products])
        return ProductCategory.objects.all()

    @property
    def gasstocks(self):
        return GASSupplierStock.objects.filter(gas=self)

    @property
    def ordered_products(self):
        return GASSupplierOrderProduct.objects.filter(order__in=self.orders)

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
        # WARNING: get GAS proxy instance!
        g = GAS.objects.get(pk=self.gas.pk)
        return g.orders

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
        # A GAS member is interested primarily to show products
        return self.gas.products

    @property
    def stocks(self):
        # A GAS member is interested primarily to show products and price
        return self.gas.stocks

    @property
    def gasstocks(self):
        # A GAS member is interested primarily in those products and price per GAS
        return self.gas.gasstocks

    def basket(self):
        return GASMemberOrder.objects.filter(product__order__in=self.orders.open())

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
        if hasattr(self, 'isfiltered') and self.isfiltered:
            return GASMember.objects.filter(pk__in=[obj.pk for obj in self.all_gasmembers])
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
    def ordered_products(self):
        return GASSupplierOrderProduct.objects.all()

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

    @property
    def pacts(self):
        return self.pact_set.all()

    @property
    def pact(self):
        return GASSupplierSolidalPact.objects.get(supplier=self)
        
    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(pact__in=self.pacts)

    @property
    def order(self):
        raise NoSenseException("calling supplier.order is a no-sense. Supplier is related to more than one order")

    @property
    def gas_list(self):
        return GAS.objects.filter(pact_set__in=self.pacts)

    @property
    def gas(self):
        raise NoSenseException("calling supplier.gas is a no-sense. Supplier is related to more than one gas")

    @property
    def des_list(self):
        return DES.objects.filter(gas_set__in=self.gas_list)

    @property
    def des(self):
        c = self.des_list.count()
        if c == 0:
            raise DoesNotExist()
        elif c == 1:
            rv = self.des_list[0]
        else:
            raise MultipleObjectsReturned()
        return rv

    @property
    def stocks(self):
        return self.stock_set.all()

    @property
    def products(self):
        """All products _supplied_ by this supplier"""
        #TODO: we have to differentiate a way to see all products __produced__ by this supplier
        return Product.objects.filter(stock_set__in=self.stocks)

    @property
    def categories(self):
        """All categories _supplied_ by this supplier"""
        #TODO: we have to differentiate a way to see all categories __produced__ by this supplier
        return ProductCategory.objects.filter(product_set__in=self.products)


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

class SupplierReferrer(SupplierReferrer):

    class Meta:
        proxy = True

    @property
    def referrers(self):
        return SupplierReferrer.objects.filter(pk=self.pk)

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

class GASMemberOrder(GASMemberOrder):

    class Meta:
        proxy = True

    @property
    def catalogs(self):
        return GASSupplierStock.objects.filter(pk=self.pk)

    @property
    def baskets(self):
        return GASMemberOrder.objects.filter(pk=self.pk)

    @property
    def basket(self):
        return self

#TODO: des, gas, supplier, person, gasmember, product, category, order

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
