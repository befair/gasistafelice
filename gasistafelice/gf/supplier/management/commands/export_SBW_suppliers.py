
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError, transaction
from django.core.files import File

from django.contrib.auth.models import User
from gasistafelice.lib.csvmanager import CSVManager
from gasistafelice.lib import get_params_from_template
from gasistafelice.supplier.models import Supplier, Product, SupplierStock, Certification, ProductCategory, ProductPU, ProductMU
from gasistafelice.gas.models import GAS, GASMember
from gasistafelice.base.models import Place, Person, Contact

import decimal

from pprint import pprint
import logging

log = logging.getLogger(__name__)

ENCODING = "iso-8859-1"
PRODUCT_MU = ProductMU.objects.get(pk=7) #Kg
PRODUCT_CAT = ProductCategory.objects.get(pk=81) #
PRODUCT_PU = ProductPU.objects.get(pk=5)  #cf
CERTIFICATION = [Certification.objects.get(pk=4)]  #Bad
STEP = 1.0

class Command(BaseCommand):

    #TODO: pass argument <gas_pk> for automatic associate a pact for the supplier list?
    args = "<supplier_csv_file> <products_csv_file> [pk][delimiter] [python_template] [python_template2] [simulate]"
    allowed_keys_1 = ['ID','Active (0/1)','Name *','Description','Short description','Meta title','Meta keywords','Meta description','ImageURL']
    allowed_keys_2 = ['ID','Active (0/1)','Name *','Categories (x,y,z...)','Price tax excluded or Price tax included','Tax rules ID','Wholesale price','On sale (0/1)','Discount amount','Discount percent','Discount from (yyyy-mm-dd)','Discount to (yyyy-mm-dd)','Reference #','Supplier reference #','Supplier','Manufacturer','EAN13','UPC','Ecotax','Width','Height','Depth','Weight','Quantity','Minimal quantity','Visibility','Additional shipping cost','Unity','Unit price','Short description','Description','Tags (x,y,z...)','Meta title','Meta keywords','Meta description','URL rewritten','Text when in stock','Text when backorder allowed','Available for order (0 = No, 1 = Yes)','Product available date','Product creation date','Show price (0 = No, 1 = Yes)','Image URLs (x,y,z...)','Delete existing images (0 = No, 1 = Yes)','Feature(Name:Value:Position)','Available online only (0 = No, 1 = Yes)','Condition','Customizable (0 = No, 1 = Yes)','Uploadable files (0 = No, 1 = Yes)','Text fields (0 = No, 1 = Yes)','Out of stock','ID / Name of shop','Advanced stock management','Depends On Stock','Warehouse']

    help = """Import supplier and products from SBW csv file. Attributes allowed in python template are:

    * supplier: """ + ",".join(allowed_keys_1) + """; 
    * products: """ + ",".join(allowed_keys_2) + """;

    They are both connected by `fake_id_supplier` which must match between both the provided documents.

    """

    def handle(self, *args, **options):
       
        self.simulate = False
        delimiter = ';'
        pk = 0
        tmpl_1 = "%(ID)s %(Active (0/1))s %(Name *)s %(Description)s %(Short description)s %(Meta title)s %(Meta keywords)s %(Meta description)s %(ImageURL)s"
        tmpl_2 = "%(ID)s %(Active (0/1))s %(Name *)s %(Categories (x,y,z...))s %(Price tax excluded or Price tax included)s %(Tax rules ID)s %(Wholesale price)s %(On sale (0/1)s %(Discount amount)s %(Discount percent)s %(Discount from (yyyy-mm-dd))s %(Discount to (yyyy-mm-dd))s %(Reference #)s %(Supplier reference #)s %(Supplier)s %(Manufacturer)s %(EAN13)s %(UPC)s %(Ecotax)s %(Width)s %(Height)s %(Depth)s %(Weight)s %(Quantity)s %(Minimal quantity)s %(Visibility)s %(Additional shipping cost)s %(Unity)s %(Unit price)s %(Short description)s %(Description)s %(Tags (x,y,z...))s %(Meta title)s %(Meta keywords)s %(Meta description)s %(URL rewritten)s %(Text when in stock)s %(Text when backorder allowed)s %(Available for order (0 = No, 1 = Yes))s %(Product available date)s %(Product creation date)s %(Show price (0 = No, 1 = Yes))s %(Image URLs (x,y,z...))s %(Delete existing images (0 = No, 1 = Yes))s %(Feature(Name:Value:Position))s %(Available online only (0 = No, 1 = Yes))s %(Condition)s %(Customizable (0 = No, 1 = Yes))s %(Uploadable files (0 = No, 1 = Yes))s %(Text fields (0 = No, 1 = Yes))s %(Out of stock)s %(ID / Name of shop)s %(Advanced stock management)s %(Depends On Stock)s %(Warehouse)s "
        try:
            csv_filename_suppliers = args[0]
            csv_filename_products = args[1]
        except:
            raise CommandError("Usage import_suppliers: %s" % (self.args))


        try:
            i = 2
            while(i < 6):
                arg = args[i].split('=')
                if arg[0] == 'delimiter':
                    delimiter = arg[1]
                elif arg[0] == 'simulate':
                    self.simulate = self._bool(arg[1], False)
                elif arg[0] == 'python_template':
                    tmpl_1 = arg[1]
                elif arg[0] == 'python_template2':
                    tmpl_2 = arg[1]
                if arg[0] == 'pk':
                   pk = arg[1]
                i += 1
        except IndexError as e:
            pass

        if pk:
            suppliers = [Supplier.objects.get(pk=pk)]
        else:
            suppliers = Supplier.objects.all()

        # [ {'':'','';''}, ]
        stocks_data = []
        suppliers_data = []
        for supplier in suppliers:
            log.info(pprint("#### ---- start new supplier export (%s)... ----####" % (supplier.pk)))

            suppliers_data.append(
                {'ID' : supplier.pk,
                 'Active (0/1)' : '1',
                 'Name *' : supplier.name,
                 'Description' : supplier.description,
                 'Short description' : '',
                 'Meta title' : '',
                 'Meta keywords' : '',
                 'Meta description' : '',
                 'ImageURL' : supplier.logo
                }
            )

            for stock in supplier.stocks:
                log.info(pprint("     %s=%s product [%s]" % (supplier ,stock , stock.pk)))
                stocks_data.append(
                    {'ID': stock.pk,
                     'Active (0/1)' : '1',
                     'Name *' : stock.name.encode('utf8'),
                     'Categories (x,y,z...)' : str(stock.supplier_category).encode('utf8') if stock.supplier_category else str(stock.product.category).encode('utf8'),
                     'Price tax excluded or Price tax included' : stock.price,
                     'Tax rules ID' : '',
                     'Wholesale price' : stock.price,
                     'On sale (0/1)' : '1',
                     'Discount amount' : '',
                     'Discount percent' : '',
                     'Discount from (yyyy-mm-dd)' : '',
                     'Discount to (yyyy-mm-dd)' : '',
                     'Reference #' : supplier.pk,
                     'Supplier reference #' : supplier.pk,
                     'Supplier' : supplier.name,
                     'Manufacturer' : supplier.name,
                     'EAN13' : '',
                     'UPC' : '',
                     'Ecotax' : '',
                     'Width' : '',
                     'Height' : '',
                     'Depth' : '',
                     'Weight' : '',
                     'Quantity' : stock.amount_available,
                     'Minimal quantity' : stock.units_minimum_amount,
                     'Visibility' : '',
                     'Additional shipping cost' : '',
                     'Unity' : '',
                     'Unit price' : stock.product.muppu ,
                     'Short description' : '',
                     #'Description' : stock.product.description.decode('utf-8').encode('ascii','replace'),
                     'Description' : '',
                     'Tags (x,y,z...)' : '',
                     'Meta title' : '',
                     'Meta keywords' : '',
                     'Meta description' : '',
                     'URL rewritten' : '',
                     'Text when in stock' : '',
                     'Text when backorder allowed' : '',
                     'Available for order (0 = No, 1 = Yes)' : int(not stock.deleted),
                     'Product available date' : '',
                     'Product creation date' : '',
                     'Show price (0 = No, 1 = Yes)' : '',
                     'Image URLs (x,y,z...)' : stock.image,
                     'Delete existing images (0 = No, 1 = Yes)' : '',
                     'Feature(Name:Value:Position)' : '',
                     'Available online only (0 = No, 1 = Yes)' : '',
                     'Condition' : '',
                     'Customizable (0 = No, 1 = Yes)' : '',
                     'Uploadable files (0 = No, 1 = Yes)' : '',
                     'Text fields (0 = No, 1 = Yes)' : '',
                     'Out of stock' : int(stock.deleted),
                     'ID / Name of shop' : supplier.name,
                     'Advanced stock management' : '',
                     'Depends On Stock' : '',
                     'Warehouse' : ''
                     }
                )

        # STEP 1: write data in files
        self._write_data(csv_filename_suppliers, delimiter,suppliers_data, tmpl_1, )
        self._write_data(csv_filename_products, delimiter, stocks_data, tmpl_2, )

        return 0

    def _write_data(self, csv_filename, delimiter, csvdata, tmpl):
      
        print "self.simulate",  self.simulate 
        if(self.simulate): 
            log.debug(pprint("SIMULATING write. Content is: %s" % csvdata))
        else:
            log.debug(pprint("WRITING on file %s. Content is: %s" % (csv_filename,csvdata)))
            f = file(csv_filename, "wb")

            fieldnames = get_params_from_template(tmpl)
            m = CSVManager(fieldnames=fieldnames, delimiter=delimiter, encoding=ENCODING)
            data = m.write(csvdata)
            #log.debug(pprint(m.read(csvdata)))

            f.write(data)

            f.close()

        return

    def _bool(self, val_d, default):
        if not val_d or val_d =='' :
            return default
        else:
            try:
                x=bool(val_d)
            except:
                return default
            else:
                return x





