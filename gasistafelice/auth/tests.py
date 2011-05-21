from django.test import TestCase

from permissions.models import Role

from gasistafelice.base.models import Place
from gasistafelice.gas.models import GAS, GASSupplierOrder, Delivery, Withdrawal
from gasistafelice.supplier.models import Supplier
from gasistafelice.auth import GAS_MEMBER, GAS_REFERRER, GAS_REFERRER_CASH, GAS_REFERRER_TECH, GAS_REFERRER_DELIVERY,\
GAS_REFERRER_WITHDRAWAL, GAS_REFERRER_SUPPLIER, GAS_REFERRER_ORDER, SUPPLIER_REFERRER 
from gasistafelice.auth import valid_params_for_roles
from gasistafelice.auth.models import ParamRole
from gasistafelice.auth.utils import register_parametric_role,\
    _validate_parametric_role

from datetime import time, date, datetime

class ParamRoleValidationTest(TestCase):
    '''Tests for the `_validate_parametric_role` function'''
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
        self.constraints = valid_params_for_roles
    def testValidationOK(self):
        '''Verify that validation of a parametric role succeeds if arguments are fine'''
        name = SUPPLIER_REFERRER
        params = {'supplier':self.supplier}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_MEMBER
        params = {'gas':self.gas}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER
        params = {'gas':self.gas}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER_CASH
        params = {'gas':self.gas}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER_TECH
        params = {'gas':self.gas}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER_SUPPLIER
        params = {'gas':self.gas, 'supplier':self.supplier}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER_ORDER
        params = {'order':self.order}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER_WITHDRAWAL
        params = {'withdrawal':self.withdrawal}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
        name = GAS_REFERRER_DELIVERY
        params = {'delivery':self.delivery}
        self.assertTrue(_validate_parametric_role(name, params, constraints=self.constraints))
    def testValidationFailIfRoleNotAllowed(self):
        '''Verify that validation of a parametric role fails if basic role isn't allowed'''
        name = 'FOO'
        params = {'gas':self.gas}
        self.assertFalse(_validate_parametric_role(name, params, constraints=self.constraints))
    def testValidationFailIfParamNameNotAllowed(self):
        '''Verify that validation of a parametric role fails if a param's name isn't allowed'''
        name = 'GAS_MEMBER'
        params = {'foo':self.gas}
        self.assertFalse(_validate_parametric_role(name, params, constraints=self.constraints))
    
    def testValidationFailIfParamTypeNotAllowed(self):
        '''Verify that validation of a parametric role fails if a param's type isn't allowed'''
        name = 'GAS_MEMBER'
        params = {'gas':self.supplier}
        self.assertFalse(_validate_parametric_role(name, params, constraints=self.constraints))    
        
    def testValidationOKIfNoConstraints(self):
        '''Verify that validation of any parametric role succeeds if no costraints are specified'''
        name = 'FOO'
        params = {'foo':None}
        self.assertTrue(_validate_parametric_role(name, params))        
        


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
        
    def testRegistrationFailIfRoleNotAllowed(self):
        '''Verify that registration of a parametric role fails if basic role isn't allowed'''
        self.assertFalse(register_parametric_role(name='FOO', gas=self.gas))
        
    def testRegistrationFailIfParamNameNotAllowed(self):
        '''Verify that registration of a parametric role fails if a param's name isn't allowed'''
        self.assertFalse(register_parametric_role(name=GAS_MEMBER, foo=self.gas))
    
    def testRegistrationFailIfParamTypeNotAllowed(self):
        '''Verify that registration of a parametric role fails if a param's type isn't allowed'''
        self.assertFalse(register_parametric_role(name=GAS_MEMBER, gas=self.supplier))
        
    def testAvoidDuplicateParamRoles(self):
        '''If a given parametric role already exists in the DB, don't duplicate it'''
        register_parametric_role(GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)
        register_parametric_role(GAS_REFERRER_SUPPLIER, gas=self.gas, supplier=self.supplier)
        self.assertEqual(ParamRole.objects.filter(role__name=GAS_REFERRER_SUPPLIER).count(), 1)

                 