"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from gasistafelice.base.models import Person
from gasistafelice.gas.models import GAS, GASMember, GASSupplierStock, GASSupplierSolidalPact
from gasistafelice.supplier.models import Supplier, ProductCategory, Product, SupplierStock
from datetime import time, date

class SimpleTest(TestCase):
    fixtures = ['test_data.json']

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)


__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True

>>> from gasistafelice.gas.models.base import *
>>> from gasistafelice.supplier.models import *
>>> g1 = GAS.objects.all()[0]
>>> gname = g1.name
>>> gname
u'Gas1'
>>> gname
u'Gas1sdfasgasga'

#>>> from gasistafelice.supplier.models import *
>>> prod = Product.objects.all()[1000]
>>> sellers = SupplierStock.objects.filter(product=prod)
>>> len(sellers)
1
>>> prod = Product.objects.all()[0]
>>> sellers = SupplierStock.objects.filter(product=prod)
>>> len(sellers)
2



"""}

class SupplierStockTest(TestCase):
    fixtures = ['test_data.json']

    def multiple_supplier_per_product(self):
        """
        Tests that product from id [1 .. 127] that is to say SupplierStock [1874 .. 2000] have 2 supplier.
        This test require fixtures
        """
        prod_multiple = Product.objects.all()[0]
        prod_unique = Product.objects.all()[1000]
        seller = SupplierStock.objects.filter(product=prod_unique)
        sellers = SupplierStock.objects.filter(product=prod_multiple)
        self.assertTrue(len(seller) < len(sellers))
        self.assertEqual(seller.supplier, sellers.supplier)





