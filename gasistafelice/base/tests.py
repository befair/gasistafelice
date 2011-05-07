from django.test import TestCase

from gasistafelice.base.models import Person, Place

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
        self.assertEqual(p.name, 'via Garibaldi, 1 - Senigallia (AN)')
    def testNameHonored(self):
        '''Verify name is honored if specified'''
        p = Place.objects.create(name='Rotonda a mare', city='senigallia', province='ancona')
        self.assertEqual(p.name, 'Rotonda a mare')