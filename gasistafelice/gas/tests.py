from django.test import TestCase
from django.contrib.auth.models import User

from permissions.models import Role

from gasistafelice.base.models import Person, Place

from gasistafelice.gas.models import GAS, GASMember, GASSupplierStock, GASSupplierSolidalPact,\
GASMemberOrder, GASSupplierOrder, GASSupplierOrderProduct, Delivery, Withdrawal
from gasistafelice.gas.managers import GASMemberManager

from gasistafelice.supplier.models import Supplier, SupplierStock, Product, ProductCategory

from gasistafelice.auth import GAS_REFERRER, GAS_REFERRER_CASH, GAS_REFERRER_TECH, GAS_REFERRER_DELIVERY,\
GAS_REFERRER_WITHDRAWAL, GAS_REFERRER_SUPPLIER, GAS_REFERRER_ORDER 
from gasistafelice.auth.models import ParamRole, Param
from gasistafelice.auth.utils import register_parametric_role

from datetime import time, date, datetime

class GASSupplierStockTest(TestCase):
    '''Test behaviour of managed attributes of GASSupplierStock'''
    
    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')        
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.category = ProductCategory.objects.create(name='food') 
        self.product = Product.objects.create(name='carrots', category=self.category, producer=self.supplier)
        self.stock = SupplierStock.objects.create(supplier=self.supplier, product=self.product, price=100)
        
    def testSupplier(self):
        '''Verify if supplier is retrieved correctly'''
        gss = GASSupplierStock.objects.create(pact=self.pact, stock=self.stock)
        self.assertEqual(gss.supplier, self.supplier)
                
    def testPrice(self):
        '''Verify if price is computed correctly'''
        pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        gss = GASSupplierStock.objects.create(pact=pact, stock=self.stock)
        pact.order_price_percent_update = 0.05
        pact.save()
        self.assertEqual(gss.price, 105)

class GASMemberOrderTest(TestCase):
    '''Test behaviour of managed attributes of GASMemberOrder

    Set of minimalistic anagrafical fixtures. In order to correct and clean setUp anagrafical data.
    In order to be more readable and focus on TestCase itself

    test.json give
        2 GAS
        each GAS have 2 gasmembers so 2 persons so 2 users
        2 Producers and 2 suppliers
        4 products
        Supplier 1 produce 2 products and sell 2 products
        Supplier 2 produce 2 products and sell 3 products (one is produce by producer 1)
        SolidalPact between
            GAS 1 <--> Supplier 1
            GAS 1 <--> Supplier 2
            GAS 2 <--> Supplier 1
            a pact can be created between GAS 2 and Supplier 2 for some TestCase

        Use runing $ python manage.py test gas.GASMemberOrderTest'''
    fixtures = ['test.json']

    def setUp(self):
        self.now = date.today()
        self.pact = GASSupplierSolidalPact.objects.get(pk=1)
        self.gas = self.pact.gas
        self.member = self.gas.gasmembers[:1].get()
        self.order = GASSupplierOrder.objects.create(pact=self.pact, date_start=self.now)
        self.orderable_product = self.order.orderable_products[0]

    def testDeliveredPrice(self):
        '''Verify if actual delivered is computed correctly by auto populate 

        in form we use el.gasstock.price'''
        self.assertIsNotNone(not self.orderable_product.delivered_price)

    def testActualPrice(self):
        '''Verify if actual price is computed correctly

        Don't be confused:
        orderable_product.initial_price: the price of the Product at the time the GASSupplierOrder was created
        orderable_product.order_price: the price of the Product at the time the GASSupplierOrder was sent to the Supplier
        orderable_product.delivered_price: the actual price of the Product (as resulting from the invoice)'''
        self.orderable_product.delivered_price = 115
        self.orderable_product.save()
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.tot_price, 115)

    def testOrder(self):
        '''Verify if SupplierOrder is computed correctly'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.order, self.order)
        
    def testGAS(self):
        '''Verify if GAS is computed correctly'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.gas, self.gas)

    def testAvoidDuplicateEntry(self):
        '''Verify that entry are unique for together purchaser and order_product'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        gmo.save()
        gmo2 = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=2)
        gmo2.save()
        gmos = GASMemberOrder.objects.filter(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product)
        self.assertEqual(gmos.count(), 1)

    def testCascadingEnablingProduct(self):
        '''TODO Enable Supplier stock and verify cascading until GASSupplierOrderProduct (Added to list).'''
        return True

    def testCascadingDisablingProduct(self):
        '''TODO Disable Supplier stock and verify cascading until GASMemberOrder (delete existing).'''
        return True

    def testControlPurchaserUserIsTheSamePerson(self):
        '''TODO in form View: the logged user cannot insert GASMemberOrder for other user.'''
        self.member2 = self.gas.gasmembers[1]
        return True


class GASSupplierOrderProductTest(TestCase):
    '''Test behaviour of managed attributes of GASSupplierOrderProduct'''
    
    def setUp(self):
        
        self.now = date.today()
        
        user1 = User.objects.create(username='Foo')
        user2 = User.objects.create(username='Bar')
        user3 = User.objects.create(username='Baz')
         
        self.person_1 = Person.objects.create(name='John', surname='Smith', user=user1)
        self.person_2 = Person.objects.create(name='Mary', surname='White', user=user2)
        self.person_3 = Person.objects.create(name='Paul', surname='Black', user=user3)
        
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_2 = GAS.objects.create(name='RiGAS', id_in_des='2')
        
        self.supplier_1 = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        self.pact_3 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_1)
        
        self.member_1 = GASMember.objects.create(person=self.person_1, gas=self.gas_1)
        self.member_2 = GASMember.objects.create(person=self.person_2, gas=self.gas_1)
        self.member_3 = GASMember.objects.create(person=self.person_3, gas=self.gas_2)
        
        self.category = ProductCategory.objects.create(name='food') 
        
        self.product_1 = Product.objects.create(name='carrots', category=self.category, producer=self.supplier_1)
        self.product_2 = Product.objects.create(name='beans', category=self.category, producer=self.supplier_1)
        
        self.stock_1 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_1, price=100)
        self.stock_2 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_2, price=150)
        self.stock_3 = SupplierStock.objects.create(supplier=self.supplier_2, product=self.product_1, price=120)
        
        self.gas_stock_1 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_1)
        self.gas_stock_2 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_2)
        self.gas_stock_3 = GASSupplierStock.objects.create(pact=self.pact_2, stock=self.stock_3)
        self.gas_stock_4 = GASSupplierStock.objects.create(pact=self.pact_3, stock=self.stock_1)
        
        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_1, date_start=self.now)
        self.order_2 = GASSupplierOrder.objects.create(pact=self.pact_3, date_start=self.now)
        
        self.product_1 = GASSupplierOrderProduct.objects.create(order=self.order_1, stock=self.gas_stock_1)
        self.product_2 = GASSupplierOrderProduct.objects.create(order=self.order_1, stock=self.gas_stock_2)
        self.product_3 = GASSupplierOrderProduct.objects.create(order=self.order_2, stock=self.gas_stock_1)
                       
        
    def testOrderedAmount(self):
        '''Verify if ordered amount is computed correctly'''
        # FIXME: perhaps a fixture would be a better way to initialize the environment 
        
        GASMemberOrder.objects.create(purchaser=self.member_1, ordered_price= self.product_1.order_price, ordered_product=self.product_1, ordered_amount=1)
        GASMemberOrder.objects.create(purchaser=self.member_1, ordered_price= self.product_2.order_price, ordered_product=self.product_2, ordered_amount=2)
        GASMemberOrder.objects.create(purchaser=self.member_2, ordered_price= self.product_1.order_price, ordered_product=self.product_1, ordered_amount=4)
        # In a real world scenario, this order shouldn't be allowed 
        # (i.e. a GAS member issuing an GASMemberOrder against a SupplierOrder opened by another GAS)
        GASMemberOrder.objects.create(purchaser=self.member_3, ordered_price= self.product_1.order_price, ordered_product=self.product_1, ordered_amount=8)
        GASMemberOrder.objects.create(purchaser=self.member_3, ordered_price= self.product_3.order_price, ordered_product=self.product_3, ordered_amount=16)
        
        self.assertEqual(self.product_1.ordered_amount, 5)
        
    def testGas(self):
        '''Verify if gas attribute is computed correctly'''
        product = GASSupplierOrderProduct.objects.create(order=self.order_1, stock=self.gas_stock_1)
        self.assertEqual(product.gas, self.gas_1)
        
class GASSupplierOrderTest(TestCase):
    '''Tests GASSupplierOrder methods'''
    def setUp(self):
        self.now = date.today()
                       
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_2 = GAS.objects.create(name='RiGAS', id_in_des='2')        
        
        self.supplier_1 = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        self.pact_3 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_1)
        
        self.category = ProductCategory.objects.create(name='food') 
        
        self.product_1 = Product.objects.create(name='carrots', category=self.category, producer=self.supplier_1)
        self.product_2 = Product.objects.create(name='beans', category=self.category, producer=self.supplier_1)
        
        self.stock_1 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_1, price=100)
        self.stock_2 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_2, price=150)
        self.stock_3 = SupplierStock.objects.create(supplier=self.supplier_2, product=self.product_1, price=120)
        
        self.gas_stock_1 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_1)
        self.gas_stock_2 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_2)
        self.gas_stock_3 = GASSupplierStock.objects.create(pact=self.pact_2, stock=self.stock_3)

        self.gas_stock_4 = GASSupplierStock.objects.create(pact=self.pact_3, stock=self.stock_1)
        
                
    def testDefaultProductSet(self):
        '''Verify that the default product set is correctly generated'''
        order = GASSupplierOrder.objects.create(pact=self.pact_1, date_start=self.now)
        order.set_default_stock_set()
        self.assertEqual(set(order.stock_set.all()), set((self.gas_stock_1, self.gas_stock_2)))
        
class GASMemberManagerTest(TestCase):
    """
    Tests for the `GASMemberManager` manager class
    """

    def setUp(self):
        today = date.today()
        now = datetime.now()        
        midnight = time(hour=0)
        
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_2 = GAS.objects.create(name='barGAS', id_in_des='2')
        
        self.person_1 = Person.objects.create(name='Mario', surname='Rossi')
        self.person_2 = Person.objects.create(name='Carlo', surname='Bianchi')
        self.person_3 = Person.objects.create(name='Antonio', surname='Verdi')
        self.person_4 = Person.objects.create(name='Giorgio', surname='Rosi')
        
        self.user_1 = User.objects.create(username='Foo')
        self.user_2 = User.objects.create(username='Bar')
        self.user_3 = User.objects.create(username='Baz')
        self.user_4 = User.objects.create(username='Spam')
        
        self.person_1.user=self.user_1
        self.person_1.save()
        self.person_2.user=self.user_2
        self.person_2.save()
        self.person_3.user=self.user_3
        self.person_3.save()
        self.person_4.user=self.user_4
        self.person_4.save()
        
        
        self.member_1 = GASMember.objects.create(gas=self.gas_1, person=self.person_1)
        self.member_2 = GASMember.objects.create(gas=self.gas_2, person=self.person_2)
        self.member_3 = GASMember.objects.create(gas=self.gas_1, person=self.person_3)
        self.member_4 = GASMember.objects.create(gas=self.gas_2, person=self.person_3)
        self.member_5 = GASMember.objects.create(gas=self.gas_1, person=self.person_4)
        
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')  
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier)
        
        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_1, date_start=today)
        self.order_2 = GASSupplierOrder.objects.create(pact=self.pact_2, date_start=today)
        
        self.place = Place.objects.create(city='senigallia', province='AN')
        
        self.delivery = Delivery.objects.create(place=self.place, date=today)
        
        self.withdrawal = Withdrawal.objects.create(place=self.place, date=today, start_time=now, end_time=midnight)
    
    def testShallowCopyOk(self):
        """It should be possible to make a shallow copy of a manager instance"""
        # see https://docs.djangoproject.com/en/1.3/topics/db/managers/#implementation-concerns
        import copy
        manager = GASMemberManager()
        my_copy = copy.copy(manager)
        self.assertEqual(manager, my_copy)
    
    def testGasReferrersOK(self):
        """
        Only GAS members having a 'GAS Referrer' role in the GAS they belongs to should be returned.    
        """
        
        self.p_role_1 = register_parametric_role(GAS_REFERRER, gas=self.gas_1)
        self.p_role_2 = register_parametric_role(GAS_REFERRER, gas=self.gas_2)
            
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.gas_referrers()), set((self.member_1, self.member_2, self.member_3)))
        
    def testTechReferrersOK(self):
        """
        Only GAS members having a 'Tech Referrer' role in the GAS they belongs to should be returned.    
        """
        
        self.p_role_1 = register_parametric_role(GAS_REFERRER_TECH, gas=self.gas_1)
        self.p_role_2 = register_parametric_role(GAS_REFERRER_TECH, gas=self.gas_2)
            
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.tech_referrers()), set((self.member_1, self.member_2, self.member_3)))
    
    def testCashReferrersOK(self):
        """
        Only GAS members having a 'Cash Referrer' role in the GAS they belongs to should be returned.    
        """
        
        self.p_role_1 = register_parametric_role(GAS_REFERRER_CASH, gas=self.gas_1)  
        self.p_role_2 = register_parametric_role(GAS_REFERRER_CASH, gas=self.gas_2)
        
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.tech_referrers()), set((self.member_1, self.member_2, self.member_3)))
    
    def testSupplierAgentsOK(self):
        """
        Only GAS members having a 'Supplier Referrer' role in the GAS they belongs to should be returned.    
        """
        self.role, created = Role.objects.get_or_create(name=GAS_REFERRER_SUPPLIER)   
        
        self.p_role_1 = register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact_1)
        self.p_role_2 = register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact_2)
                
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.supplier_referrers()), set((self.member_1, self.member_2, self.member_3)))
    
    def testOrderReferrersOK(self):
        """
        Only GAS members having a 'Order Referrer' role in the GAS they belongs to should be returned.    
        """
        
        self.p_role_1 = register_parametric_role(GAS_REFERRER_ORDER, order=self.order_1)
        self.p_role_2 = register_parametric_role(GAS_REFERRER_ORDER, order=self.order_2)
              
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.order_referrers()), set((self.member_1, self.member_2, self.member_3)))
    
    def testDeliveryReferrersOK(self):
        """
        Only GAS members having a 'Delivery Referrer' role in the GAS they belongs to should be returned.    
        """
      
        self.p_role_1 = register_parametric_role(GAS_REFERRER_DELIVERY, delivery=self.delivery)
        self.p_role_2 = register_parametric_role(GAS_REFERRER_DELIVERY, delivery=self.delivery)
           
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.delivery_referrers()), set((self.member_1, self.member_2, self.member_3)))
    
    def testWithdrawalReferrersOK(self):
        """
        Only GAS members having a 'Withdrawal Referrer' role in the GAS they belongs to should be returned.    
        """
        
        self.p_role_1 = register_parametric_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self.withdrawal)
        self.p_role_2 = register_parametric_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self.withdrawal)
        
        self.p_role_1.add_principal(self.user_1)
        self.p_role_1.add_principal(self.user_3)
        self.p_role_2.add_principal(self.user_2)
        
        self.assertEqual(set(GASMember.objects.withdrawal_referrers()), set((self.member_1, self.member_2, self.member_3)))



#__test__ = {"doctest": """
#
#>>> from gasistafelice.gas.models.base import *
#>>> from gasistafelice.supplier.models import *
#>>> g1 = GAS.objects.all()[0]
#>>> gname = g1.name
#>>> gname
#u'Gas1'
#>>> gname
#u'Gas1sdfasgasga'
#
##>>> from gasistafelice.supplier.models import *
#>>> prod = Product.objects.all()[1000]
#>>> sellers = SupplierStock.objects.filter(product=prod)
#>>> len(sellers)
#1
#>>> prod = Product.objects.all()[0]
#>>> sellers = SupplierStock.objects.filter(product=prod)
#>>> len(sellers)
#2
#
#
#
#"""}
#
#class SupplierStockTest(TestCase):
#    """
#    Tests for the `GASMemberManager` manager class
#    """
#    fixtures = ['test_data.json']
#
#    def multiple_supplier_per_product(self):
#        """
#        Tests that product from id [1 .. 127] that is to say SupplierStock [1874 .. 2000] have 2 supplier.
#        This test require fixtures
#        """
#        prod_multiple = Product.objects.all()[0]
#        prod_unique = Product.objects.all()[1000]
#        seller = SupplierStock.objects.filter(product=prod_unique)
#        sellers = SupplierStock.objects.filter(product=prod_multiple)
#        self.assertTrue(len(seller) < len(sellers))
#        self.assertEqual(seller.supplier, sellers.supplier)
