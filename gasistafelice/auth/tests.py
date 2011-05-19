from django.test import TestCase

from permissions.models import Role

from gasistafelice.base.models import Place
from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal
from gasistafelice.supplier.models import Supplier
from gasistafelice.auth import GAS_MEMBER, GAS_REFERRER, GAS_REFERRER_CASH, GAS_REFERRER_TECH, GAS_REFERRER_DELIVERY, GAS_REFERRER_WITHDRAWAL, GAS_REFERRER_SUPPLIER, GAS_REFERRER_ORDER 
from gasistafelice.auth.models import ParamRole
from gasistafelice.auth.utils import register_parametric_role

from datetime import time, date, datetime


class ParamRoleRegistrationTest(TestCase):
    '''Tests for the `register_parametric_role` function'''
    def setUp(self):
        now = datetime.now()
        today = date.today()        
        midnight = time(hour=0)
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.order = GASSupplierOrder.objects.create(gas=self.gas, supplier=self.supplier, date_start=today)
        self.place = Place.objects.create(city='senigallia', province='AN')
        self.delivery = Delivery.objects.create(place=self.place, date=today)
        self.withdrawal = Withdrawal.objects.create(place=self.place, date=today, start_time=now, end_time=midnight)
            
    def testRegistrationOK(self):
        '''Verify that registration of a parametric role succeeds if arguments are fine'''
        # register a parametric GAS member
        register_parametric_role(GAS_MEMBER, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_MEMBER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_MEMBER) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS referrer
        register_parametric_role(GAS_REFERRER, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS cash referrer
        register_parametric_role(GAS_REFERRER_CASH, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_CASH).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_CASH) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS tech referrer
        register_parametric_role(GAS_REFERRER_TECH, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_TECH).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_TECH) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS supplier referrer
        register_parametric_role(GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_SUPPLIER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_SUPPLIER) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(set(param_names), set(['gas','supplier']))
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(set(param_values), set([self.gas,self.supplier]))
        
        # register a parametric GAS order referrer
        register_parametric_role(GAS_REFERRER_ORDER, order=self.order)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_ORDER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_ORDER) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['order',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.order,])
        
        # register a parametric GAS withdrawal referrer
        register_parametric_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self.withdrawal)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_WITHDRAWAL).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_WITHDRAWAL) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['withdrawal',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.withdrawal,])
        
        # register a parametric GAS delivery referrer
        register_parametric_role(GAS_REFERRER_DELIVERY, delivery=self.delivery)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_DELIVERY).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_DELIVERY) 
        param_names = [p.name for p in pr.param_set.all()]
        self.assertEqual(param_names, ['delivery',])
        param_values = [p.param for p in pr.param_set.all()]
        self.assertEqual(param_values, [self.delivery,])
                 