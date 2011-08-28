from django.test import TestCase
from django.contrib.auth.models import User, Group 

from permissions.models import Role

from gasistafelice.base.models import Place, Person
from gasistafelice.gas.models import GAS, GASMember, GASSupplierOrder, Delivery, Withdrawal, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier

from gasistafelice.auth import GAS_MEMBER, GAS_REFERRER, GAS_REFERRER_CASH, GAS_REFERRER_TECH, GAS_REFERRER_DELIVERY,\
GAS_REFERRER_WITHDRAWAL, GAS_REFERRER_SUPPLIER, GAS_REFERRER_ORDER, SUPPLIER_REFERRER 
from gasistafelice.auth import VALID_PARAMS_FOR_ROLES
from gasistafelice.auth.models import ParamRole, Param, PrincipalParamRoleRelation
from gasistafelice.auth.utils import register_parametric_role, _validate_parametric_role,\
_parametric_role_as_dict, _is_valid_parametric_role_dict_repr,\
    _compare_parametric_roles
from gasistafelice.auth.exceptions import RoleNotAllowed, RoleParameterNotAllowed, RoleParameterWrongSpecsProvided
from gasistafelice.auth.managers import RoleManager


from datetime import time, date, datetime

class ParamByNameTest(TestCase):
    """Tests if parameters of a parametric role can be accessed by name"""
    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        
        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
        
        self.role = Role.objects.create(name='FOO')   
        p_role= ParamRole.objects.create(role=self.role)
        p1 = Param.objects.create(name='gas', value=self.gas)
        p_role.param_set.add(p1)
        p2 = Param.objects.create(name='supplier', value=self.supplier)
        p_role.param_set.add(p2)
        p_role.save()
        self.p_role = p_role 
            
    def testGetOK(self):
        """Verify that an existing parameter can be retrieved by its name"""
        p_role = self.p_role
        self.assertEqual(p_role.gas, self.gas)
        self.assertEqual(p_role.supplier, self.supplier) 
    
    def testGetFailIfParameterNotSet(self):
        """When trying to retrieve an unset parameter, `None` should be returned"""
        p_role = self.p_role
        self.assertIsNone(p_role.order)
    
    def testGetErrorIfInvalidParameter(self):
        """When trying to retrieve a non-allowed parameter, AttributeError should be raised"""
        p_role = self.p_role
        self.assertRaises(AttributeError, getattr, p_role, 'foo')
    

class ParamRoleAsDictTest(TestCase):
    """Tests for the `_parametric_role_as_dict()` helper function"""
    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.role = Role.objects.create(name='FOO')
        
        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
        
        p_role= ParamRole.objects.create(role=self.role)
        p1 = Param.objects.create(name='gas', value=self.gas)
        p_role.param_set.add(p1)
        p2 = Param.objects.create(name='supplier', value=self.supplier)
        p_role.param_set.add(p2)
        
        p_role.save()
        self.p_role = p_role
        
    def testConversionOK(self):
        """If a ParamRole instance is passed, return a dictionary representing it"""
        expected_dict = {'role':self.role, 'params':{'gas':self.gas, 'supplier':self.supplier}}
        self.assertEqual(_parametric_role_as_dict(self.p_role), expected_dict)
        
    def testConversionFail(self):
        """If the argument isn't a ParamRole instance, raise a TypeError"""
        self.assertRaises(TypeError, _parametric_role_as_dict, None)
        self.assertRaises(TypeError, _parametric_role_as_dict, 1)
        self.assertRaises(TypeError, _parametric_role_as_dict, self.role)
    
    
class ParamRoleAsDictValidationTest(TestCase):
    """Tests for the `_is_valid_parametric_role_dict_repr()` helper function"""
    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.role = Role.objects.create(name='FOO')        
        
    def testValidationOK(self):
        """If a dictionary has the right structure to represent a parametric role, return True"""
        p_role_dict = {'role':self.role, 'params':{'gas':self.gas, 'supplier':self.supplier}}
        self.assertTrue(_is_valid_parametric_role_dict_repr(p_role_dict))
    
    def testValidationFailIfNotDict(self):
        """If passed dictionary hasn't expected keys, return False"""
        p_role_dict = {'foo':self.role, 'params':{'gas':self.gas, 'supplier':self.supplier}}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))
        p_role_dict = {'role':self.role, 'foo':{'gas':self.gas, 'supplier':self.supplier}}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))
        p_role_dict = {'role':self.role, 'params':{'gas':self.gas, 'supplier':self.supplier}, 'foo':None}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))
        
    def testValidationFailIfNotRole(self):
        """If `role` key is not a `Role` model instance, return False"""
        p_role_dict = {'role':1, 'params':{'gas':self.gas, 'supplier':self.supplier}}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))        
    
    def testValidationFailIfNotParams(self):
        """If `params` key is not a dictionary, return False"""
        p_role_dict = {'role':self.role, 'params':1}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))  

class ParamRoleComparisonTest(TestCase):
    """Tests for the `_compare_parametric_roles()` helper function"""
    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_1 = GAS.objects.create(name='barGAS', id_in_des='2')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        
        self.role = Role.objects.create(name='FOO')
        self.role_1 = Role.objects.create(name='BAR')
        
        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
                
        self.p1 = Param.objects.create(name='gas', value=self.gas)
        self.p2 = Param.objects.create(name='supplier', value=self.supplier)
        self.p3 = Param.objects.create(name='gas', value=self.gas_1)
        
        p_role_1 = ParamRole.objects.create(role=self.role)
        p_role_1.param_set.add(self.p1)
        p_role_1.param_set.add(self.p2)        
        p_role_1.save()
        self.p_role_1 = p_role_1
        
        p_role_2 = ParamRole.objects.create(role=self.role)
        p_role_2.param_set.add(self.p1)
        p_role_2.param_set.add(self.p2)        
        p_role_2.save()
        self.p_role_2 = p_role_2    
        
        p_role_3 = ParamRole.objects.create(role=self.role_1)
        p_role_3.param_set.add(self.p1)
        p_role_3.param_set.add(self.p2)        
        p_role_3.save()
        self.p_role_3 = p_role_3    
        
        p_role_4 = ParamRole.objects.create(role=self.role)
        p_role_4.param_set.add(self.p3)
        p_role_4.param_set.add(self.p2)        
        p_role_4.save()
        self.p_role_4 = p_role_4    
            
        
    def testComparisonOK(self):
        """If arguments describe the same parametric role, return True"""         
        # compare two ParamRole instances
        self.assertTrue(_compare_parametric_roles(self.p_role_1, self.p_role_2))
                
        # compare two dictionary representations
        p_role_dict_1 = {'role':self.role, 'params':{'gas':self.gas, 'supplier':self.supplier}}
        p_role_dict_2 = {'role':self.role, 'params':{'supplier':self.supplier, 'gas':self.gas}}
        self.assertTrue(_compare_parametric_roles(p_role_dict_1, p_role_dict_2))
        
        # compare one ParamRole instance and one dictionary representation
        self.assertTrue(_compare_parametric_roles(p_role_dict_1, self.p_role_2))
        self.assertTrue(_compare_parametric_roles(p_role_dict_2, self.p_role_1))
        
    def testFailIfNotSameKind(self):
        """If arguments describe parametric roles of different kind, return False"""
        
        self.assertFalse(_compare_parametric_roles(self.p_role_1, self.p_role_3))
    
    def testFailIfNotSameParameters(self):
        """If arguments describe parametric roles with different parameters, return False"""
        self.assertFalse(_compare_parametric_roles(self.p_role_1, self.p_role_4))        
    
    def testErrorIfTooManyArguments(self):
        """If more than two arguments are given, raise TypeError"""
        self.assertRaises(TypeError, _compare_parametric_roles, self.p_role_1, self.p_role_2, self.p_role_2)
        self.assertRaises(TypeError, _compare_parametric_roles, self.p_role_1, self.p_role_2, None)

    def testErrorIfNotEnoughArguments(self):
        """If less than two arguments are given, raise TypeError"""
        
        self.assertRaises(TypeError, _compare_parametric_roles, self.p_role_1)
        self.assertRaises(TypeError, _compare_parametric_roles)

    def testErrorIfInvalidArguments(self):
        """If an argument is neither a ParamRole instance nor a valid dictionary representation for it, raise TypeError"""
        
        self.assertRaises(TypeError, _compare_parametric_roles, self.p_role_1, None)
        self.assertRaises(TypeError, _compare_parametric_roles, None, self.p_role_1)
        self.assertRaises(TypeError, _compare_parametric_roles, self.p_role_1, {})
        self.assertRaises(TypeError, _compare_parametric_roles,  {}, self.p_role_1)


class ParamRoleValidationTest(TestCase):
    """Tests for the `_validate_parametric_role` function"""
    def setUp(self):
        now = datetime.now()
        today = date.today()        
        midnight = time(hour=0)
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.order = GASSupplierOrder.objects.create(pact=self.pact, date_start=today)
        self.place = Place.objects.create(city='senigallia', province='AN')
        self.delivery = Delivery.objects.create(place=self.place, date=today)
        self.withdrawal = Withdrawal.objects.create(place=self.place, date=today, start_time=now, end_time=midnight)
        self.constraints = VALID_PARAMS_FOR_ROLES
    def testValidationOK(self):
        """Verify that validation of a parametric role succeeds if arguments are fine"""
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
        """Verify that validation of a parametric role fails if basic role isn't allowed"""
        name = 'FOO'
        params = {'gas':self.gas}
        self.assertRaises(RoleNotAllowed, _validate_parametric_role, name, params, constraints=self.constraints)
    def testValidationFailIfParamNameNotAllowed(self):
        """Verify that validation of a parametric role fails if a param's name isn't allowed"""
        name = 'GAS_MEMBER'
        params = {'foo':self.gas}
        self.assertRaises(RoleParameterNotAllowed, _validate_parametric_role, name, params, constraints=self.constraints)
    
    def testValidationFailIfParamTypeNotAllowed(self):
        """Verify that validation of a parametric role fails if a param's type isn't allowed"""
        name = 'GAS_MEMBER'
        params = {'gas':self.supplier}
        self.assertRaises(RoleParameterWrongSpecsProvided, _validate_parametric_role, name, params, constraints=self.constraints)    
        
    def testValidationOKIfNoConstraints(self):
        """Verify that validation of any parametric role succeeds if no costraints are specified"""
        name = 'FOO'
        params = {'foo':None}
        self.assertTrue(_validate_parametric_role(name, params))        
        


class ParamRoleRegistrationTest(TestCase):
    """Tests for the `register_parametric_role` function"""
    def setUp(self):
        now = datetime.now()
        today = date.today()        
        midnight = time(hour=0)
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.order = GASSupplierOrder.objects.create(pact=self.pact, date_start=today)
        self.place = Place.objects.create(city='senigallia', province='AN')
        self.delivery = Delivery.objects.create(place=self.place, date=today)
        self.withdrawal = Withdrawal.objects.create(place=self.place, date=today, start_time=now, end_time=midnight)
            
    def testRegistrationOK(self):
        """Verify that registration of a parametric role succeeds if arguments are fine"""
        # register a parametric GAS member
        register_parametric_role(GAS_MEMBER, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_MEMBER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_MEMBER) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS referrer
        register_parametric_role(GAS_REFERRER, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS cash referrer
        register_parametric_role(GAS_REFERRER_CASH, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_CASH).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_CASH) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS tech referrer
        register_parametric_role(GAS_REFERRER_TECH, gas=self.gas)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_TECH).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_TECH) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(param_names, ['gas',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.gas,])
        
        # register a parametric GAS supplier referrer
        register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_SUPPLIER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_SUPPLIER) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(set(param_names), set(['gas','supplier']))
        param_values = [p.param for p in pr.params]
        self.assertEqual(set(param_values), set([self.gas,self.supplier]))
        
        # register a parametric GAS order referrer
        register_parametric_role(GAS_REFERRER_ORDER, order=self.order)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_ORDER).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_ORDER) 
        param_names = [p.name for p in pr.params]        
        self.assertEqual(param_names, ['order',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.order,])
        
        # register a parametric GAS withdrawal referrer
        register_parametric_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self.withdrawal)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_WITHDRAWAL).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_WITHDRAWAL) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(param_names, ['withdrawal',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.withdrawal,])
        
        # register a parametric GAS delivery referrer
        register_parametric_role(GAS_REFERRER_DELIVERY, delivery=self.delivery)
        # check that Role object has been created in the db
        self.assertEqual(Role.objects.filter(name=GAS_REFERRER_DELIVERY).count(), 1)
        # check that a ParamRole with the right parameters has been created in the db
        pr = ParamRole.objects.get(role__name=GAS_REFERRER_DELIVERY) 
        param_names = [p.name for p in pr.params]
        self.assertEqual(param_names, ['delivery',])
        param_values = [p.param for p in pr.params]
        self.assertEqual(param_values, [self.delivery,])
        
    def testRegistrationFailIfRoleNotAllowed(self):
        """Verify that registration of a parametric role fails if basic role isn't allowed"""
        self.assertRaises(RoleNotAllowed, register_parametric_role, name='FOO', gas=self.gas)
        
    def testRegistrationFailIfParamNameNotAllowed(self):
        """Verify that registration of a parametric role fails if a param's name isn't allowed"""
        self.assertRaises(RoleParameterNotAllowed, register_parametric_role, name=GAS_MEMBER, foo=self.gas)
    
    def testRegistrationFailIfParamTypeNotAllowed(self):
        """Verify that registration of a parametric role fails if a param's type isn't allowed"""
        self.assertRaises(RoleParameterWrongSpecsProvided, register_parametric_role, name=GAS_MEMBER, gas=self.supplier)
        
    def testAvoidDuplicateParamRoles(self):
        """If a given parametric role already exists in the DB, don't duplicate it"""
        register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact)
        register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact)
        self.assertEqual(ParamRole.objects.filter(role__name=GAS_REFERRER_SUPPLIER).count(), 1)
        
class RoleAutoSetupTest(TestCase):
    """Tests automatic role-setup operations happening at instance-creation time"""
    def setUp(self):
        now = datetime.now()
        today = date.today()        
        midnight = time(hour=0)
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
        self.order = GASSupplierOrder.objects.create(pact=self.pact, date_start=today)
        self.place = Place.objects.create(city='senigallia', province='AN')
        self.delivery = Delivery.objects.create(place=self.place, date=today)
        self.withdrawal = Withdrawal.objects.create(place=self.place, date=today, start_time=now, end_time=midnight)
        self.pact = GASSupplierSolidalPact.objects.create(gas=self.gas, supplier=self.supplier)
    
    def testGASRoleSetup(self):
        """Verify that GAS-specific parametric roles are created when a new GAS is created"""
        # GAS_REFERRER_TECH, GAS_REFERRER_CASH
        

        role, created = Role.objects.get_or_create(name=GAS_MEMBER)
        p_role = ParamRole.objects.get(role__name=GAS_MEMBER)
        expected_dict = {'role':role, 'params':{'gas':self.gas}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)

        role, created = Role.objects.get_or_create(name=GAS_REFERRER_CASH)
        p_role = ParamRole.objects.get(role__name=GAS_REFERRER_CASH)
        expected_dict = {'role':role, 'params':{'gas':self.gas}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)

        role, created = Role.objects.get_or_create(name=GAS_REFERRER_TECH)
        p_role = ParamRole.objects.get(role__name=GAS_REFERRER_TECH)
        expected_dict = {'role':role, 'params':{'gas':self.gas}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)
     

    def testGASMemberRoleSetup(self):
        """Verify that role-related setup tasks are executed when a new GAS member is created"""
        # TODO
        pass
        
    def testGASSupplierSolidalPactRoleSetup(self):
        """Verify that a parametric GAS_REFERRER_SUPPLIER is created when a new solidal pact is created"""
        # GAS_REFERRER_SUPPLIER
        
        role, created = Role.objects.get_or_create(name=GAS_REFERRER_SUPPLIER)
        p_role = ParamRole.objects.get(role__name=GAS_REFERRER_SUPPLIER)
        expected_dict = {'role':role, 'params': {'pact':self.pact}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)

    def testGASSupplierOrderRoleSetup(self):
        """Verify that a parametric GAS_REFERRER_ORDER is created when a new GAS supplier order is created"""
        role, created = Role.objects.get_or_create(name=GAS_REFERRER_ORDER)
        p_role = ParamRole.objects.get(role__name=GAS_REFERRER_ORDER)
        expected_dict = {'role':role, 'params': {'order':self.order}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)

        
    def testDeliveryRoleSetup(self):
        """Verify that a parametric GAS_REFERRER_DELIVERY is created when a new delivery appointment is created"""
        role, created = Role.objects.get_or_create(name=GAS_REFERRER_DELIVERY)
        p_role = ParamRole.objects.get(role__name=GAS_REFERRER_DELIVERY)
        expected_dict = {'role':role, 'params': {'delivery':self.delivery}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)

    
    def testWithdrawalRoleSetup(self):
        """Verify that a parametric GAS_REFERRER_WITHDRAWAL is created when a new withdrawal appointment is created"""
        role, created = Role.objects.get_or_create(name=GAS_REFERRER_WITHDRAWAL)
        p_role = ParamRole.objects.get(role__name=GAS_REFERRER_WITHDRAWAL)
        expected_dict = {'role':role, 'params': {'withdrawal':self.withdrawal}}
        self.assertEqual(_parametric_role_as_dict(p_role), expected_dict)

class AddParamRoleToPrincipalTest(TestCase):
    """Tests `ParamRole.add_principal()` method"""
    
    def setUp(self):
        self.user = User.objects.create(username='Foo')
        self.group = Group.objects.create(name='Foo')
        
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        
        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
        
        self.role = Role.objects.create(name='FOO')
        p_role = ParamRole.objects.create(role=self.role)
        p1 = Param.objects.create(name='gas', value=self.gas)
        p_role.param_set.add(p1)
        p2 = Param.objects.create(name='supplier', value=self.supplier)
        p_role.param_set.add(p2)        
        p_role.save()
        self.p_role = p_role
                       
    
    def testAddToUserOK(self):
        """Verify that if a User instance is passed, the parametric role gets assigned to that user"""
        self.p_role.add_principal(self.user)
        self.assertEqual(PrincipalParamRoleRelation.objects.filter(user=self.user, role=self.p_role).count(), 1) 
    
    def testAddToGroupOK(self):
        """Verify that if a Group instance is passed, the parametric role gets assigned to that group"""
        self.p_role.add_principal(self.group)
        self.assertEqual(PrincipalParamRoleRelation.objects.filter(group=self.group, role=self.p_role).count(), 1) 
    
    def testAddFail(self):
        """If neither a User nor a Group instance is passed, raise `TypeError`"""
        self.assertRaises(TypeError, self.p_role.add_principal)
        self.assertRaises(TypeError, self.p_role.add_principal, 1)
        self.assertRaises(TypeError, self.p_role.add_principal, self.gas)
        
class ParamRoleGetUsersTest(TestCase):
    """Tests `ParamRole.get_users()` method"""
    
    def setUp(self):
        self.user1 = User.objects.create(username='Foo')
        self.user2 = User.objects.create(username='Bar')
        self.user3 = User.objects.create(username='Baz')
        
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')
        
        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
                
        self.role = Role.objects.create(name='FOO')   
        p_role= ParamRole.objects.create(role=self.role)
        p1 = Param.objects.create(name='gas', value=self.gas)
        p_role.param_set.add(p1)
        p2 = Param.objects.create(name='supplier', value=self.supplier)
        p_role.param_set.add(p2)
        p_role.save()
        self.p_role = p_role 
        
    def testGetUsersOK(self):
        """Verify that all the users this parametric role was assigned to are returned"""
        self.p_role.add_principal(self.user1)
        self.p_role.add_principal(self.user2)
        prrs = PrincipalParamRoleRelation.objects.filter(role=self.p_role)
        users = [prr.user for prr in prrs if prr.user is not None]
        self.assertEqual(set(users), set((self.user1, self.user2)) )
        
    # TODO: add tests for local roles
        
class ParamRoleGetGroupsTest(TestCase):
    """Tests `ParamRole.get_groups()` method"""
    
    def setUp(self):
        self.group1 = Group.objects.create(name='Foo')
        self.group2 = Group.objects.create(name='Bar')
        self.group3 = Group.objects.create(name='Baz')
        
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')

        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
                
        self.role = Role.objects.create(name='FOO')   
        p_role= ParamRole.objects.create(role=self.role)
        p1 = Param.objects.create(name='gas', value=self.gas)
        p_role.param_set.add(p1)
        p2 = Param.objects.create(name='supplier', value=self.supplier)
        p_role.param_set.add(p2)
        p_role.save()
        self.p_role = p_role 
    
        
        
    def testGetGroupsOK(self):
        """Verify that all the groups this parametric role was assigned to are returned"""
        self.p_role.add_principal(self.group1)
        self.p_role.add_principal(self.group2)
        prrs = PrincipalParamRoleRelation.objects.filter(role=self.p_role)
        groups = [prr.group for prr in prrs if prr.group is not None]
        self.assertEqual(set(groups), set((self.group1, self.group2)))
        
    # TODO: add tests for local roles
class PrincipalRoleRelationTest(TestCase):
    """Tests for the `PrincipalRoleRelation` methods"""  
    def setUp(self):
        self.user = User.objects.create(username='Foo')
        self.user1 = User.objects.create(username='Bar')
        self.group = Group.objects.create(name='Foo')
        self.group1 = Group.objects.create(name='Bar')
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.supplier = Supplier.objects.create(name='Acme inc.', vat_number='123')

        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        Param.objects.all().delete()
        ParamRole.objects.all().delete()        
        
        self.role = Role.objects.create(name='FOO')   
        p_role= ParamRole.objects.create(role=self.role)
        p1 = Param.objects.create(name='gas', value=self.gas)
        p_role.param_set.add(p1)
        p2 = Param.objects.create(name='supplier', value=self.supplier)
        p_role.param_set.add(p2)
        p_role.save()
        self.p_role = p_role 
    
    def testGetPrincipalOK(self):
        """Tests if the principal (user or group) is correctly retrieved"""
        prr = PrincipalParamRoleRelation.objects.create(user=self.user, role=self.p_role)
        self.assertEqual(prr.get_principal(), self.user)
        prr = PrincipalParamRoleRelation.objects.create(group=self.group, role=self.p_role)
        self.assertEqual(prr.get_principal(), self.group)        
        
    def testSetPrincipalOK(self):
        """Tests if the principal (user or group) is correctly set"""
        prr = PrincipalParamRoleRelation.objects.create(user=self.user, role=self.p_role)
        prr.set_principal(self.user1)
        self.assertEqual(prr.user, self.user1)
        
        prr = PrincipalParamRoleRelation.objects.create(group=self.group, role=self.p_role)
        prr.set_principal(self.group1)
        self.assertEqual(prr.group, self.group1)
            
        prr = PrincipalParamRoleRelation.objects.create(user=self.user, role=self.p_role)
        prr.set_principal(self.group)
        self.assertEqual(prr.group, self.group)        
        
        prr = PrincipalParamRoleRelation.objects.create(group=self.group, role=self.p_role)
        prr.set_principal(self.user)
        self.assertEqual(prr.user, self.user)
        
        
    def testSetPrincipalError(self):
        """If neither a User nor a Group instance is passed, raise `TypeError`"""
        pass    
    
    
            
class RoleManagerTest(TestCase):
    """Tests for the `RoleManager` manager class"""  

    def setUp(self):
        self.gas = GAS.objects.create(name='fooGAS', id_in_des='1')
        self.gas_1 = GAS.objects.create(name='barGAS', id_in_des='2')
        self.gas_2 = GAS.objects.create(name='bazGAS', id_in_des='3')
        
        self.supplier = Supplier.objects.create(name='SmallCompany', vat_number='111')
        self.supplier_1 = Supplier.objects.create(name='Acme inc.', vat_number='123')
        self.supplier_2 = Supplier.objects.create(name='GoodCompany', vat_number='321')
        
        self.pact_1 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_1)
        self.pact_2 = GASSupplierSolidalPact.objects.create(gas=self.gas_1, supplier=self.supplier_2)
        self.pact_3 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_1)
        self.pact_4 = GASSupplierSolidalPact.objects.create(gas=self.gas_2, supplier=self.supplier_2)
        
              
        # cleanup existing ParamRoles (e.g. those auto-created at model instance's creation time)
        ParamRole.objects.all().delete()
        
        # A member of GAS 1
        self.p_role_1 = register_parametric_role(GAS_MEMBER, gas=self.gas_1) 
        # A member of GAS 2
        self.p_role_2 = register_parametric_role(GAS_MEMBER, gas=self.gas_2)
        # A supplier referrer for GAS 1 and supplier 1
        self.p_role_3 = register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact_1)
        # A supplier referrer for GAS 1 and supplier 2
        self.p_role_4 = register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact_2)
        # A supplier referrer for GAS 2 and supplier 1
        self.p_role_5 = register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact_3)
        # A supplier referrer for GAS 2 and supplier 2
        self.p_role_6 = register_parametric_role(GAS_REFERRER_SUPPLIER, pact=self.pact_4)
        
    def testShallowCopyOk(self):
        """It should be possible to make a shallow copy of a manager instance"""
        # see https://docs.djangoproject.com/en/1.3/topics/db/managers/#implementation-concerns
        import copy
        manager = RoleManager()
        my_copy = copy.copy(manager)
        self.assertEqual(manager, my_copy)
    
                    
    def testGetParamRolesOK(self):
        """Check that `get_param_roles` returns the right set of parametric roles if input is valid"""  
        self.assertEqual(set(ParamRole.objects.get_param_roles(role_name=GAS_MEMBER)), set((self.p_role_1, self.p_role_2))) 
        self.assertEqual(set(ParamRole.objects.get_param_roles(role_name=GAS_MEMBER, gas=self.gas_1)), set((self.p_role_1, )))
        
        self.assertEqual(set(ParamRole.objects.get_param_roles(role_name=GAS_REFERRER_SUPPLIER)),\
        set((self.p_role_3, self.p_role_4, self.p_role_5, self.p_role_6)))
        self.assertEqual(set(ParamRole.objects.get_param_roles(role_name=GAS_REFERRER_SUPPLIER, pact=self.pact_1)),\
        set((self.p_role_3)))
        
    
    def testGetParamRolesFailIfInvalidRole(self):
        """Check that `get_param_roles` fails as expected if given an invalid role name"""  
        self.assertRaises(RoleNotAllowed, ParamRole.objects.get_param_roles, role_name='FOO', gas=self.gas)    
    
    def testGetParamRolesFailIfInvalidParamName(self):
        """Check that `get_param_roles` fails as expected if the name of parameter is invalid"""  
        self.assertRaises(RoleParameterNotAllowed, ParamRole.objects.get_param_roles, role_name=GAS_MEMBER, foo=self.gas)
    
    def testGetParamRolesFailIfInvalidParamType(self):
        """Check that `get_param_roles` fails as expected if the value of parameter is of the wrong type"""  
        self.assertRaises(RoleParameterWrongSpecsProvided, ParamRole.objects.get_param_roles, role_name=GAS_MEMBER, gas=self.supplier)
        
    