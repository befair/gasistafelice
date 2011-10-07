from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User 

from gasistafelice.base.models import Person, Place
from gasistafelice.base.utils import get_ctype_from_model_label

class PersonSaveTest(TestCase):
    '''Tests for the Person save override method'''
    def testCapitalize(self):
        '''Verify name and surname are capitalized on save'''
        p = Person.objects.create(name='john', surname='smith')
        self.assertEqual(p.name, 'John')
        self.assertEqual(p.surname, 'Smith')
    def testUuidAutoset(self):
        '''Verify an empty UUID is autoset to None on save'''
        p = Person.objects.create(name='john', surname='smith', uuid='')
        self.assertEqual(p.uuid, None)
    def testUuidHonored(self):
        '''Verify UUID is honored if specified'''
        p = Person.objects.create(name='john', surname='smith', uuid='1')
        self.assertEqual(p.uuid, '1')
        
        
class PlaceSaveTest(TestCase):
    '''Tests for the Place save override method'''
    def testCapitalize(self):
        '''Verify city and province are capitalized on save'''
        p = Place.objects.create(city='senigallia', province='an')
        self.assertEqual(p.city, 'Senigallia')
        self.assertEqual(p.province, 'AN')
    def testNameAutoset(self):
        '''Verify a missing name is correctly autoset on save'''
        p = Place.objects.create(city='senigallia', province='an', address='via Garibaldi, 1')
        self.assertEqual(p.name, 'via Garibaldi, 1')
    def testNameHonored(self):
        '''Verify name is honored if specified'''
        p = Place.objects.create(name='Rotonda a mare', city='senigallia', province='ancona')
        self.assertEqual(p.name, 'Rotonda a mare')
        

class GetCtypeFromModelLabelTest(TestCase):
    '''Tests for the `get_ctype_from_model_label()` function'''
    def setUp(self):        
            pass
    def testOK(self):
        '''Verify the right ContentType is returned if the model label is good'''
        user_ct = ContentType.objects.get_for_model(User)
        ct = get_ctype_from_model_label('auth.User')
        self.assertEqual(ct, user_ct)
    def testMalformedLabel(self):
        '''Return None if the label is malformed'''
        ct = get_ctype_from_model_label('auth:User')
        self.assertIsNone(ct)
        
    def testModelNotExisting(self):
        '''Return None if the label points to a non existing model'''
        ct = get_ctype_from_model_label('auth.Foo')
        self.assertIsNone(ct)
        
