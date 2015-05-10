
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
    args = "<supplier_csv_file> <products_csv_file> [delimiter] [python_template] [python_template2] [simulate]"
    allowed_keys_1 = ['ID','Active (0/1)','Name *','Description','Short description','Meta title','Meta keywords','Meta description','ImageURL']
    allowed_keys_2 = ['ID','Active (0/1)','Name *','Categories (x,y,z...)','Price tax excluded or Price tax included','Tax rules ID','Wholesale price','On sale (0/1)','Discount amount','Discount percent','Discount from (yyyy-mm-dd)','Discount to (yyyy-mm-dd)','Reference #','Supplier reference #','Supplier','Manufacturer','EAN13','UPC','Ecotax','Width','Height','Depth','Weight','Quantity','Minimal quantity','Visibility','Additional shipping cost','Unity','Unit price','Short description','Description','Tags (x,y,z...)','Meta title','Meta keywords','Meta description','URL rewritten','Text when in stock','Text when backorder allowed','Available for order (0 = No, 1 = Yes)','Product available date','Product creation date','Show price (0 = No, 1 = Yes)','Image URLs (x,y,z...)','Delete existing images (0 = No, 1 = Yes)','Feature(Name:Value:Position)','Available online only (0 = No, 1 = Yes)','Condition','Customizable (0 = No, 1 = Yes)','Uploadable files (0 = No, 1 = Yes)','Text fields (0 = No, 1 = Yes)','Out of stock','ID / Name of shop','Advanced stock management','Depends On Stock','Warehouse']

    help = """Import supplier and products from SBW csv file. Attributes allowed in python template are:

    * supplier: """ + ",".join(allowed_keys_1) + """; 
    * products: """ + ",".join(allowed_keys_2) + """;

    They are both connected by `fake_id_supplier` which must match between both the provided documents.

    """

    def handle(self, *args, **options):
       
        simulate = False
        delimiter = ';'
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
                    simulate = self._bool(arg[1], False)
                elif arg[0] == 'python_template':
                    tmpl_1 = arg[1]
                elif arg[0] == 'python_template2':
                    tmpl_2 = arg[1]
                i += 1
        except IndexError as e:
            pass

        # STEP 0: prepare data in dicts
        data_suppliers = self._prepare_data(csv_filename_suppliers, delimiter, tmpl_1)
        data_products = self._prepare_data(csv_filename_products, delimiter, tmpl_2)

        # Data prepared
        with transaction.atomic():
            i = 0
            sum_sup = 0
            sum_pro = 0
            sum_pro_all = 0
            for sup_d in data_suppliers:
                i += 1
                try:
                    log.info(pprint("#### ---- start new supplier import (%s)... ----####" % (i)))
                    sum_sup += 1
                    sum_pro = 0
                    log.info(pprint("-------------Supplier(%s) [%s]" % (sum_sup, sup_d['Name *'])))

                    s = Supplier(
                        name=sup_d['Name *'],
                        website='',
                        iban='',
                        description=sup_d['Description'],
                        logo=sup_d['ImageURL'],
                    )

                    if not simulate:
                        s.save()
                        log.info(pprint(("CREATED Supplier %s with pk [%s]" % (s,s.pk)).decode(ENCODING)))
                    else:
                        log.info(pprint(("SIMULATED Supplier %s with pk [%s]" % (s,s.pk)).decode(ENCODING)))

                    for product_d in data_products:
                        try:
                            sup_name = sup_d['Name *']
                            pro_name = product_d['Manufacturer']
                            if pro_name != sup_name:
                                continue
                            else:
                                sum_pro += 1
                                sum_pro_all += 1
                                log.info(pprint("     %s=%s product [%s]   (%s-%s-%s)" % (sup_name ,pro_name ,product_d['Name *'], sum_sup, sum_pro, sum_pro_all)))

                                p = Product(
                                    name=product_d['Name *'],
                                    producer=s,
                                    category= self._get_category(product_d['Categories (x,y,z...']),
                                    mu=self._get_mu(None),
                                    pu=self._get_pu(None),
                                    muppu=self._avoid_empty(None,None),
                                )
                                
                                if not simulate:
                                    p.save()
                                    log.info(pprint("CREATED Product with pk: [%s]" % p.pk))
                                else:
                                    log.info(pprint("SIMULATED Product with pk: [%s]" % p.pk))

                                log.info(pprint("PASS Product %s step(%s)" % (p.pk, product_d['Minimal quantity'])))
                                
                                s_s = SupplierStock(
                                    product=p,
                                    supplier=s,
                                    amount_available=product_d['Quantity'],
                                    detail_step=product_d['Minimal quantity'],
                                    price=decimal.Decimal(self._avoid_empty(product_d['Price tax excluded or Price tax included'], 0.0)),
                                )

                                if not simulate:
                                    s_s.save()
                                    log.info(pprint("CREATED SupplierStock with pk: [%s]" % s_s.pk))
                                else:
                                    log.info(pprint("SIMULATED SupplierStock with pk: [%s]" % s_s.pk))


                                log.info(pprint("PASS SupplierStock %s " % (s_s.pk)))

                        except KeyError, e:
                            raise CommandError("Product Key '%s' is REQUIRED." % e.message)

                except KeyError, e:
                    raise CommandError("Supplier Key '%s' is REQUIRED." % e.message)

        return 0

    def _prepare_data(self, csv_filename, delimiter, tmpl):

        f = file(csv_filename, "rb")
        csvdata = f.read()
        f.close()

        fieldnames = get_params_from_template(tmpl)
        m = CSVManager(fieldnames=fieldnames, delimiter=delimiter, encoding=ENCODING)
        data = m.read(csvdata)
        log.debug(pprint(m.read(csvdata)))

        return data

    def _avoid_empty(self, val_d, default):
        if not val_d or val_d =='' :
            return default
        else:
            return val_d

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

    def _get_pu(self, val_d, default):
        if not val_d or val_d == '' :
            return default
        try:
            x=ProductPU.objects.get(pk=int(val_d))
        except:
            return default
        else:
            return x

    def _get_pu(self, val_d):
        if not val_d or val_d == '' :
            return PRODUCT_PU
        try:
            x=ProductPU.objects.get(pk=int(val_d))
        except:
            return PRODUCT_PU
        else:
            return x

    def _get_mu(self, val_d):
        if not val_d or val_d == '' :
            return PRODUCT_MU
        try:
            x=ProductMU.objects.get(pk=int(val_d))
        except:
            return PRODUCT_MU
        else:
            return x

    def _get_category(self, val_d):
        if not val_d or val_d == '' :
            return PRODUCT_CAT
        try:
            x=ProductCategory.objects.get(pk=int(val_d))
        except:
            return PRODUCT_CAT
        else:
            return x

    #def _get_pretty(self, val_d, default):
    #    #PrettyDecimalField
    #    #FIXME: django.core.exceptions.ValidationError: [u'This value must be a decimal number.']
    #    log.info(pprint("error params get_step (%s) --> %s----" % (val_d, default)))
    #    if not val_d or val_d == '' :
    #        return default
    #    try:
    #        #x=decimal.Decimal(val_d)
    #        #FOR TEST ONLY
    #        x=int(val_d)
    #    except:
    #        return default
    #    else:
    #        log.info(pprint("error get_step (%s) --> %s----" % (val_d, x)))
    #        return x
