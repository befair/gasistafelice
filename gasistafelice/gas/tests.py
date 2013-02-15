from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management.commands import dumpdata
from django.test.client import Client

from permissions.models import Role

from gasistafelice.base.models import Person, Place

from gasistafelice.des.management.commands import init_superuser

from gasistafelice.gas.models import GAS, GASMember, GASSupplierStock, GASSupplierSolidalPact,\
GASMemberOrder, GASSupplierOrder, GASSupplierOrderProduct, Delivery, Withdrawal
from gasistafelice.gas.managers import GASMemberManager

from gasistafelice.supplier.models import Supplier, SupplierStock, Product, ProductCategory, ProductPU

from gasistafelice.consts import * 
from flexi_auth.models import ParamRole, Param
from flexi_auth.utils import register_parametric_role

from datetime import time, date, datetime
from django.db import IntegrityError
from decimal import Decimal

from lib import views_support

class TestWithClient(TestCase):

    USERNAME = "gasista"
    TEST_PASSWORD = "felice"

    def setUp(self):

        # Create test user
        self._user = self.create_user(username=self.USERNAME)

        self._c = Client()

    def create_user(self, username=None):
        """Make the user able to login."""
        user = User.objects.create(
            username=[self.USERNAME, username][bool(username)]
        )
        user.set_password(self.TEST_PASSWORD)
        user.save()
        return user

    def create_user_unloggable(self, username=None):
        """Create user with no password --> cannot login"""
        user = User.objects.create(
            username=[self.USERNAME, username][bool(username)]
        )
        return user

    def _logout(self):
        self._c.logout()

    def _login(self, user=None):
        """Login a user.

        If user is None, login the default user
        """

        self._logout()
        login_user = [self._user, user][bool(user)]
        rv = self._c.login(username=login_user.username, password=self.TEST_PASSWORD)
        return rv

    def _check_for_error_response(self, response, e=Exception):
        """HTTP response is always 200, context_data 'http_status_code' tells the truth"""
        self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
        self.assertEqual(
            response.context_data['http_status_code'], 
            views_support.HTTP_ERROR_INTERNAL
        )
        self.assertEqual(response.context_data['exception_type'], e)

    def _check_for_success_response(self, response, is_ajax=True):
        """HTTP response is always 200, context_data 'http_status_code' tells the truth"""
        if is_ajax:
            self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
            self.assertEqual(
                response.context_data['http_status_code'], 
                views_support.HTTP_SUCCESS
            )
        else:
            self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
    
    def _check_for_redirect_response(self,response, is_ajax=False):
        """ HTTP response is 302, in case the server redirects to another page"""
        if is_ajax:
            self.assertEqual(response.status_code, views_support.HTTP_SUCCESS)
            self.assertEqual(
                response.context_data['http_status_code'], 
                views_support.HTTP_REDIRECT
            )
        else:
            self.assertEqual(response.status_code, views_support.HTTP_REDIRECT)

    def _POST(self, url, is_ajax, **kwargs):
        
        if is_ajax:
            response = self._c.post(url,
                kwargs,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        else:
            response = self._c.post(url,
                kwargs
            )
        return response

    def _GET(self, url, is_ajax, **kwargs):

        if is_ajax:
            response = self._c.get(url,
                kwargs,
                HTTP_X_REQUESTED_WITH='XMLHttpRequest'
            )
        else:
            response = self._c.get(url,
                kwargs
            )
        return response

class GASSupplierStockTest(TestCase):
    '''Test behaviour of managed attributes of GASSupplierStock'''

    fixtures=['des_test_data.json']

    def setUp(self):
        self.place_1 = Place.objects.create(name="fooGAS headquarter")
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1', headquarter=self.place_1)
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.category = ProductCategory.objects.create(name='food')
        self.productPU = ProductPU.objects.create(name='unit',symbol='u',description='produt unit')
        self.product = Product.objects.create(name='carrots', category=self.category, producer=self.supplier, pu=self.productPU)
        self.stock = SupplierStock.objects.create(supplier=self.supplier, product=self.product, price=100)
        
    def testSupplier(self):
        '''Verify if supplier is retrieved correctly'''
        #This is automatically created from GASSupplierSolidalPact setup_data. Here we have to GET it.
        #gss = GASSupplierStock.objects.create(pact=self.pact, stock=self.stock)
        gss = GASSupplierStock.objects.get(pact=self.pact, stock=self.stock)
        self.assertEqual(gss.supplier, self.supplier)
                
    def testPrice(self):
        '''Verify if price is computed correctly'''
        pact = GASSupplierSolidalPact.objects.get(gas=self.gas, supplier=self.supplier)
        #This is automatically created from GASSupplierSolidalPact setup_data. Here we have to GET it.
        #gss = GASSupplierStock.objects.create(pact=pact, stock=self.stock)
        gss = GASSupplierStock.objects.get(pact=pact, stock=self.stock)
        pact.order_price_percent_update = Decimal('0.05')
        pact.save()
        self.assertEqual(gss.price, 105)

class GASMemberOrderTest(TestCase):
    '''Test behaviour of managed attributes of GASMemberOrder'''


    fixtures = ['a_test_auth.json','b_test_des.json',
                'c_test_sites_site.json','d_test_users_userprofile.json',
                'e_test_workflows.json','f_test_base.json',
                'g_test_supplier.json','h_test_gas.json',
                'i_test_simpleaccounting.json'
    ]

    def setUp(self):
        self.now = date.today()
        self.pact = GASSupplierSolidalPact.objects.get(pk=1)
        self.gas = self.pact.gas
        self.member = self.gas.gasmembers[:1].get()
        self.order = GASSupplierOrder.objects.get(pk=1)
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
        self.orderable_product.order_price = 115
        self.orderable_product.save()
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.price_expected, 115)

    def testDeliveryPrice(self):
        '''Verify if delivery price is computed correctly'''
        self.orderable_product.order_price = 115
        self.orderable_product.delivery_price = 100
        self.orderable_product.save()
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.price_expected, 115)
        self.assertEqual(gmo.ordered_product.delivery_price, 100)

    def testTotalPrice(self):
        '''Verify if total price is computed correctly'''
        self.orderable_product.order_price = 100
        self.orderable_product.save()
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=2)
        self.assertEqual(gmo.price_expected, 2 * gmo.ordered_price)
        self.assertEqual(gmo.price_expected, 2 * gmo.ordered_product.order_price)

    def testOrder(self):
        '''Verify if SupplierOrder is computed correctly'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.order, self.order)
        
    def testGAS(self):
        '''Verify if GAS is computed correctly'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        self.assertEqual(gmo.gas, self.gas)

    def testDuplicateEntryRaiseError(self):
        '''Verify that entry are unique for together purchaser and order_product
        '''
        from django.db import connection
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        gmo.save()
        gmos = GASMemberOrder.objects.filter(purchaser=self.member, ordered_product=self.orderable_product)
        self.assertEqual(gmos.count(), 1)
        error_ocurred = False
        try: 
            #should raise an exception IntegrityError: (1062, "Duplicate entry '1-1' for key 'ordered_product_id'")
            gmo2 = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=2)
            gmo2.save()
        except IntegrityError as e:
            error_ocurred = True
        self.assertTrue(error_ocurred)
        # Raise `DatabaseError: current transaction is aborted, commands ignored until end of transaction block`
        #gmos = GASMemberOrder.objects.filter(purchaser=self.member, ordered_product=self.orderable_product)
        #self.assertEqual(gmos.count(), 1)

    def testIsConfirmed(self):
        '''Verify if gmo confirmation depend of GAS configuration'''
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        gmo.save()
        gmos = GASMemberOrder.objects.filter(purchaser=self.member, ordered_product=self.orderable_product)
        self.assertEqual(gmos.count(), 1)
        self.assertEqual(gmo.purchaser.gas.config.gasmember_auto_confirm_order, self.gas.config.gasmember_auto_confirm_order)
        self.assertEqual(gmo.is_confirmed, self.gas.config.gasmember_auto_confirm_order)

    def testManualIsConfirmed(self):
        '''Verify that gmo must be confirmed manually if requested by GAS configuration'''
        self.gas.config.gasmember_auto_confirm_order = False;
        self.gas.config.save()
        self.gas.save()
        gmo = GASMemberOrder.objects.create(purchaser=self.member, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=1)
        gmo.save()
        self.assertEqual(GAS.objects.get(pk=gmo.purchaser.gas.pk).config.gasmember_auto_confirm_order, self.gas.config.gasmember_auto_confirm_order)
        self.assertFalse(gmo.is_confirmed)

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
    
    fixtures=['des_test_data.json']

    def setUp(self):
        
        self.now = date.today()

        from gasistafelice.gas.workflow_data import workflow_dict
        import workflows
        #manually initialasing workflows, this is done after syncdb:
        # post_syncdb.connect(init_workflows, sender=workflows.models)
        for name, w in workflow_dict.items():
            w.register_workflow()
            print "Workflow %s was successfully registered." % name

  
        #initialasing superuser

        cmd = init_superuser.Command()
        cmd.handle()
 
        user1 = User.objects.create(username='Foo')
        user2 = User.objects.create(username='Bar')
        user3 = User.objects.create(username='Baz')
         
        self.person_1 = Person.objects.create(name='John', surname='Smith', user=user1)
        self.person_2 = Person.objects.create(name='Mary', surname='White', user=user2)
        self.person_3 = Person.objects.create(name='Paul', surname='Black', user=user3)
        
        self.place_1 = Place.objects.create(name="fooGAS headquarter")
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1', headquarter=self.place_1)
        self.place_2 = Place.objects.create(name="RiGAS headquarter")
        self.gas_2 = GAS.objects.create(name='RiGAS', id_in_des='2', headquarter=self.place_2)
        
        self.supplier_1 = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        self.pact_3 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_1)
        
        self.member_1 = GASMember.objects.create(person=self.person_1, gas=self.gas_1)
        self.member_2 = GASMember.objects.create(person=self.person_2, gas=self.gas_1)
        self.member_3 = GASMember.objects.create(person=self.person_3, gas=self.gas_2)
        
        self.category = ProductCategory.objects.create(name='food') 
        
        self.productPU = ProductPU.objects.create(name='unit',symbol='u',description='produt unit')

        self.product_1 = Product.objects.create(name='carrots', category=self.category, producer=self.supplier_1, pu=self.productPU)
        self.product_2 = Product.objects.create(name='beans', category=self.category, producer=self.supplier_1, pu=self.productPU)
        
        self.stock_1 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_1, price=100)
        self.stock_2 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_2, price=150)
        self.stock_3 = SupplierStock.objects.create(supplier=self.supplier_2, product=self.product_1, price=120)
        
        #These are automatically created from GASSupplierSolidalPact setup_data. Here we have to GET them.
        #self.gas_stock_1 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_1)
        #self.gas_stock_2 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_2)
        #self.gas_stock_3 = GASSupplierStock.objects.create(pact=self.pact_2, stock=self.stock_3)
        #self.gas_stock_4 = GASSupplierStock.objects.create(pact=self.pact_3, stock=self.stock_1)
        self.gas_stock_1 = GASSupplierStock.objects.get(pact=self.pact_1, stock=self.stock_1)
        self.gas_stock_2 = GASSupplierStock.objects.get(pact=self.pact_1, stock=self.stock_2)
        self.gas_stock_3 = GASSupplierStock.objects.get(pact=self.pact_2, stock=self.stock_3)
        self.gas_stock_4 = GASSupplierStock.objects.get(pact=self.pact_3, stock=self.stock_1)
        
        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_1, datetime_start=self.now, referrer_person=self.person_1)
        self.order_2 = GASSupplierOrder.objects.create(pact=self.pact_3, datetime_start=self.now, referrer_person=self.person_2)
        
        self.product_1 = GASSupplierOrderProduct.objects.create(order=self.order_1, gasstock=self.gas_stock_1, initial_price="12.4", order_price="12")
        self.product_2 = GASSupplierOrderProduct.objects.create(order=self.order_1, gasstock=self.gas_stock_2, initial_price="4.3", order_price="4")
        self.product_3 = GASSupplierOrderProduct.objects.create(order=self.order_2, gasstock=self.gas_stock_1, initial_price="3.1", order_price="3")

        self.orderable_product = self.order_1.orderable_products[0]
        #code useful to dump test data
        #file_open = open("test_data.json", "w")
 
        #cmd = dumpdata.Command()
        #file_open.write(cmd.handle())
        #file_open.close()
        
    def testOrderedAmount(self):
        '''Verify if ordered amount is computed correctly'''
 
        GASMemberOrder.objects.create(purchaser=self.member_1, ordered_price= self.product_1.order_price, ordered_product=self.product_1, ordered_amount=1)
        GASMemberOrder.objects.create(purchaser=self.member_1, ordered_price= self.product_2.order_price, ordered_product=self.product_2, ordered_amount=2)
        GASMemberOrder.objects.create(purchaser=self.member_2, ordered_price= self.product_1.order_price, ordered_product=self.product_1, ordered_amount=4)
        # In a real world scenario, this order shouldn't be allowed 
        # (i.e. a GAS member issuing an GASMemberOrder against a SupplierOrder opened by another GAS)
        GASMemberOrder.objects.create(purchaser=self.member_3, ordered_price= self.product_1.order_price, ordered_product=self.product_1, ordered_amount=8)
        GASMemberOrder.objects.create(purchaser=self.member_3, ordered_price= self.product_3.order_price, ordered_product=self.product_3, ordered_amount=16)

        self.assertEqual(self.product_1.tot_amount, 13)
        self.assertEqual(self.product_2.tot_amount, 2)
        self.assertEqual(self.product_3.tot_amount, 16)

    def testGas(self):
        '''Verify if gas attribute is computed correctly'''
        gmo2 = GASMemberOrder.objects.create(purchaser=self.member_1, ordered_price= self.orderable_product.order_price, ordered_product=self.orderable_product, ordered_amount=2)

        product = GASSupplierOrderProduct.objects.create(order=self.order_1, gasstock=self.gas_stock_1, initial_price="0.35", order_price="0.35")
        self.assertEqual(product.gas, self.gas_1)

class GASSupplierOrderTest(TestClient):
    '''Tests GASSupplierOrder methods'''

    fixtures = ['a_test_auth.json','b_test_des.json',
                'c_test_sites_site.json','d_test_users_userprofile.json',
                'e_test_workflows.json','f_test_base.json',
                'g_test_supplier.json','h_test_gas.json',
                'i_test_simpleaccounting.json'
    ]

    def setUp(self):
        self.now = date.today()

        self.place_1 = Place.objects.get(name="Foogas headquarter")
        self.gas_1 = GAS.objects.get(name='fooGAS', id_in_des='1', headquarter=self.place_1)
        #self.place_2 = Place.objects.create(name="RiGAS headquarter")
        #self.gas_2 = GAS.objects.create(name='RiGAS', id_in_des='2', headquarter=self.place_2)        
        
        self.supplier_1 = Supplier.objects.get(name='Acme inc.', vat_number='123')
        #self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.get(gas=self.gas_1, supplier=self.supplier_1)
        #self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        
        #self.category = ProductCategory.objects.create(name='food') 
 
        #self.productPU = ProductPU.objects.create(name='unit',symbol='u',description='produt unit')
       
        #self.product_1 = Product.objects.create(name='carrots', category=self.category, producer=self.supplier_1, pu=self.productPU)
        #self.product_2 = Product.objects.create(name='beans', category=self.category, producer=self.supplier_1, pu=self.productPU)
        #
        #self.stock_1 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_1, price=100)
        #self.stock_2 = SupplierStock.objects.create(supplier=self.supplier_1, product=self.product_2, price=150)
        
        #These are automatically created from GASSupplierSolidalPact setup_data. Here we have to GET them.
        #self.gas_stock_1 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_1)
        #self.gas_stock_2 = GASSupplierStock.objects.create(pact=self.pact_1, stock=self.stock_2)
        self.gas_stock_1 = GASSupplierStock.objects.get(pact=self.pact_1, stock=self.stock_1)
        self.gas_stock_2 = GASSupplierStock.objects.get(pact=self.pact_1, stock=self.stock_2)

        
    def testDefaultProductSet(self):
        '''Verify that the default product set is correctly generated'''
        order = GASSupplierOrder.objects.create(pact=self.pact_1, datetime_start=self.now)
        order.set_default_gasstock_set()
        self.assertEqual(set(order.stock_set.all()), set((self.gas_stock_1, self.gas_stock_2)))

class IntergasTest(TestCase):
    """ Test for orders shared between several (more than one) GAS """

    fixtures = ['a_test_auth.json','b_test_des.json',
                'c_test_sites_site.json','d_test_users_userprofile.json',
                'e_test_workflows.json','f_test_base.json',
                'g_test_supplier.json','h_test_gas.json',
                'i_test_simpleaccounting.json'
    ]

    def setUp(self):
        self.now = date.today()

        self.place_1 = Place.objects.get(name="Foogas headquarter")
        self.place_2 = Place.objects.get(name="Bargas headquarter")
        self.gas_1 = GAS.objects.get(name='fooGAS', id_in_des='1', headquarter=self.place_1)
        self.gas_2 = GAS.objects.get(name='barGAS', id_in_des='2', headquarter=self.place_2)
        
        self.supplier_1 = Supplier.objects.get(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.get(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.get(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.get(gas=self.gas_2, supplier=self.supplier_1)
        self.pact_3 = GASSupplierSolidalPact.objects.get(gas=self.gas_1, supplier=self.supplier_2)

        self.person_1 = Person.objects.get(name='Mario', surname='Rossi')
        self.person_2 = Person.objects.get(name='Carlo', surname='Bianchi')

        self.user_1 = User.objects.get(username='Bar')
        self.user_2 = User.objects.get(username='Bar')

        pr = ParamRole.get_role('GAS_REFERRER_SUPPLIER', pact=self.pact_2)
        pr.add_principal(self.user_1)

        pr = ParamRole.get_role('GAS_REFERRER_SUPPLIER', pact=self.pact_3)
        pr.add_principal(self.user_2)

    def testIntergasOrder(self):
        """ Test intergas order between two GAS 

        GAS#1 open an intergas order with GAS#2

        Here is assumed that GAS#2 has a pact with the same supplier GAS#1
        opened the order
        """

        self.gas_1.config.intergas_connection_set.add(self.gas_2)

        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_1, datetime_start=self.now, referrer_person=self.person_1)

        supplier = self.pact_1.supplier
        gas_2_has_pact = True
        try:
            extra_pact = self.gas_2.pacts.get(supplier=supplier)
        except GASSupplierSolidalPact.DoesNotExist as e:
            gas_2_has_pact = False

        self.assertTrue(gas_2_has_pact)

        if gas_2_has_pact:        
            new_order = self.order_1.clone()
            new_order.pact = extra_pact 

            # retrieve the first referrer_person
            refs = extra_pact.referrers_people
            refs_found = True
            if len(refs):
                print("refs %s found for pact %s" % (refs, extra_pact))
                new_order.referrer_person = refs[0]
                new_order.delivery_referrer_person = new_order.referrer_person
                new_order.withdrawal_referrer_person = new_order.referrer_person
            else:
                print("no referrers for pact %s" % extra_pact)
                refs_found = False

            self.assertTrue(refs_found)

            delivery = Delivery.objects.none()
            if self.order_1.delivery:

                dd_place = extra_pact.gas.config.default_delivery_place or \
                    extra_pact.gas.headquarter
                delivery, created = Delivery.objects.get_or_create(
                        date=obj.delivery.date, place=dd_place
                )
                new_order.delivery = delivery

            self.order_1.group_id = GASSupplierOrder.objects.get_new_intergas_group_id()

            new_order_saved = True
            try:
                new_order.save()
                print("created another intergas order: %s " % new_order)
            except Exception as e:
                print("repeat another NOT created: pact %s, start %s , end %s , delivery %s" % (
                    new_order.pact, new_order.datetime_start, new_order.datetime_end, 
                    new_order.delivery.date
                ))
                new_order_saved = False

            self.assertTrue(new_order_saved)

            intergas_order_ok= True
            try:
                if delivery:
                    intergas_order = GASSupplierOrder.objects.get(pact=self.pact_2, 
                        datetime_start=self.now, 
                        referrer_person=refs[0],
                        delivery=delivery
                    )
                else:
                    intergas_order = GASSupplierOrder.objects.get(pact=self.pact_2, 
                        datetime_start=self.now, 
                        referrer_person=refs[0]
                    )
            except GASSupplierOrder.DoesNotExist as e:
                intergas_order_ok = False

            self.assertTrue(intergas_order_ok)

    def testIntergasOrderNoCommonSupplier(self):
        """ Test intergas order between two GAS 

        GAS#1 open an intergas order with GAS#2

        Testthe behaviour of the code when two GAS 
        have not at least a pact each with the same 
        supplier
        """

        self.gas_1.config.intergas_connection_set.add(self.gas_2)

        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_3, datetime_start=self.now, referrer_person=self.person_2)

        supplier = self.pact_3.supplier
        gas_2_has_pact = True
        try:
            extra_pact = self.gas_2.pacts.get(supplier=supplier)
        except GASSupplierSolidalPact.DoesNotExist as e:
            gas_2_has_pact = False

        self.assertEqual(gas_2_has_pact, False)


class GASMemberManagerTest(TestCase):
    """
    Tests for the `GASMemberManager` manager class
    """

    fixtures = ['des_test_data.json']

    def setUp(self):
        today = date.today()
        now = datetime.now()        
        midnight = time(hour=0)

        from gasistafelice.gas.workflow_data import workflow_dict
        import workflows
        #manually initialasing workflows, this is done after syncdb:
        # post_syncdb.connect(init_workflows, sender=workflows.models)
        for name, w in workflow_dict.items():
            w.register_workflow()
            print "Workflow %s was successfully registered." % name

  
        #initialasing superuser

        cmd = init_superuser.Command()
        cmd.handle()
       
 
        self.place_1 = Place.objects.create(name="fooGAS headquarter")
        self.gas_1 = GAS.objects.create(name='fooGAS', id_in_des='1', headquarter=self.place_1)
        self.place_2 = Place.objects.create(name="barGAS headquarter")
        self.gas_2 = GAS.objects.create(name='barGAS', id_in_des='2', headquarter=self.place_2)
        
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

        #need to add a (eligible) referrer for the pact
        pr1 = ParamRole.get_role('GAS_REFERRER_SUPPLIER', pact=self.pact_1)

        pr1.add_principal(self.user_1)
        pr1.add_principal(self.user_2)


        self.order_1 = GASSupplierOrder.objects.create(pact=self.pact_1, datetime_start=today, referrer_person=self.person_1)
        self.order_2 = GASSupplierOrder.objects.create(pact=self.pact_2, datetime_start=today, referrer_person=self.person_2)
        
        self.place = Place.objects.create(name="foo", city='senigallia', province='AN')
        
        self.delivery = Delivery.objects.create(place=self.place, date=today)
        
        self.withdrawal = Withdrawal.objects.create(place=self.place, date=today, start_time=now, end_time=midnight)

        #code useful to dump test data
        #file_open = open("test_data_for_des", "w")
 
        #cmd = dumpdata.Command()
        #file_open.write(cmd.handle())
        #file_open.close()

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

        #print("\nset_1: %s\nset_2: %s" % (set(GASMember.objects.cash_referrers()), set((self.member_1, self.member_2, self.member_3))))
 
        self.assertEqual(set(GASMember.objects.cash_referrers()), set((self.member_1, self.member_2, self.member_3)))
    
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
