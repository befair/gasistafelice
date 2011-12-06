
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
    args = "<supplier_csv_file> <products_csv_file> [delimiter] [python_template] [python_template2]"
    allowed_keys_1 = ['fake_id_supplier','name','flavour','city','phone','email', 'address','certification','website', 'iban', 'n_employers', 'vat_number', 'ssn', 'image', 'description']
    allowed_keys_2 = ['fake_id_supplier','name','price','vat','pu','mu', 'muppu','category','code', 'units_minimum_amount', 'units_per_box', 'detail_minimum_amount', 'detail_step']

    help = """Import supplier and products from csv file. Attributes allowed in python template are:

    * supplier: """ + ",".join(allowed_keys_1) + """; 
    * products: """ + ",".join(allowed_keys_2) + """;

    They are both connected by `fake_id_supplier` which must match between both the provided documents.

    """

    def handle(self, *args, **options):
        
        try:
            csv_filename_suppliers = args[0]
            csv_filename_products = args[1]
        except:
            raise CommandError("Usage import_suppliers: %s" % (self.args))

        if len(args) > 2:
            delimiter = args[2]
        else:
            delimiter = ";"

        if len(args) == 4:
            tmpl_1 = args[3]
        else:
            tmpl_1 = "%(fake_id_supplier)s %(name)s %(flavour)s %(city)s %(phone)s %(email)s  %(address)s %(certification)s %(website)s %(iban)s %(n_employers)s %(vat_number)s %(ssn)s %(image)s %(description)s"

        if len(args) == 5:
            tmpl_2 = args[4]
        else:
            tmpl_2 = "%(fake_id_supplier)s %(name)s %(price)s %(vat)s %(pu)s %(mu)s  %(muppu)s %(category)s %(code)s  %(units_minimum_amount)s  %(units_per_box)s  %(detail_minimum_amount)s %(detail_step)s"

        # STEP 0: prepare data in dicts
        data_suppliers = self._prepare_data(csv_filename_suppliers, delimiter, tmpl_1)
        data_products = self._prepare_data(csv_filename_products, delimiter, tmpl_2)

        # Data prepared
        with transaction.commit_on_success():
            i = 0
            sum_sup = 0
            sum_pro = 0
            sum_pro_all = 0
            for sup_d in data_suppliers:
                i += 1
                try:
                    #log.info(pprint("#### ---- start new supplier import (%s)... ----####\n --> %s" % (i, sup_d)))
                    log.info(pprint("#### ---- start new supplier import (%s)... ----####" % (i)))
                    sups = Supplier.objects.filter(name__icontains=sup_d['name'])
                    if sups.count():
                        print "Found suppliers with name %s" % sups.values('name')
                        continue
                        #raise CommandError("Found suppliers with name %s" % sups.values('name'))

                    else:
                        sum_sup += 1
                        sum_pro = 0
                        log.info(pprint("-------------Supplier(%s) [%s]" % (sum_sup, sup_d['name'])))

                        #'phone','email'
                        contacts = self._get_or_create_contacts(sup_d)
                        #'city','address'
                        place = self._get_or_create_place(sup_d)

#{"pk":81,"model":"supplier.supplier", "fields": {"name":"Ittingrosso","website":"","flavour":" COOPERATING","seat":89,"vat_number": " 1336220437" ,"contact_set": [81,162,405] ,"certifications": [4]  ,"frontman": 82 } },
                        s = Supplier(
                            name=sup_d['name'],
                            #flavour=sup_d['flavour'],Error: Supplier Key 'choices' is REQUIRED.
                            seat=place,
                            website=sup_d['website'],
                            vat_number=sup_d['vat_number'],
                            iban=sup_d['iban'],
                            ssn=sup_d['ssn'],
                            description=sup_d['description'],
                            n_employers=self._avoid_empty(sup_d['n_employers'], None),
                            #FIXME: certifications= self._get_certification(sup_d),
                        )
                            #TODO: frontman=sup_d['name' and 'surname' --> Person],
                        s.save()
                        s.contact_set.add(*contacts)
                        log.info(pprint(("CREATED SUPPLIER %s" % s).decode(ENCODING)))

                        for product_d in data_products:
                            try:
                                sup_pk = sup_d['fake_id_supplier']
                                pro_pk = product_d['fake_id_supplier']
                                if pro_pk != sup_pk:
                                    continue
                                else:
                                    sum_pro += 1
                                    sum_pro_all += 1
                                    log.info(pprint("     %s=%s product [%s]   (%s-%s-%s)" % (sup_pk ,pro_pk ,product_d['name'], sum_sup, sum_pro, sum_pro_all)))

                                    # Create product and bind to producer(Supplier)
        #{"pk":1,"model":"supplier.product", "fields": {"name":"Olio ", "category":37, "producer":1, "mu":4, "pu":6, "muppu_is_variable":false, "vat_percent":"0.04" }  } ,
        #tmpl_2 = "%(fake_id_supplier)s %(name)s %(vat)s %(pu)s %(mu)s  %(muppu)s

                                    p = Product(
                                        name=product_d['name'],
                                        producer=s,
                                        category= self._get_category(product_d['category']),
                                        mu=self._get_mu(product_d['mu']),
                                        pu=self._get_pu(product_d['pu']),
                                        muppu=self._avoid_empty(product_d['muppu'],None),
                                        #muppu_is_variable=self._bool(product_d['muppu_is_variable'], True),
                                        vat_percent=self._avoid_empty(product_d['vat'],None),
                                    )
                                    #p.save()

                                    # Create stock and bind to product and supplier
        #{"pk": 1,"model": "supplier.supplierstock","fields": {"product": 1,"supplier":1,"amount_available":0,"price":"25.00", "units_per_box" : " 1" , "detail_minimum_amount" : "1.00" , "detail_step" :" 1.00 "  }  } , 
        #tmpl_2 = %(price)s  %(units_minimum_amount)s  %(units_per_box)s  %(detail_minimum_amount)s %(detail_step)s"
                                    log.info(pprint("PASS Product %s step(%s)" % (p.pk, product_d['detail_step'])))
                
                                    s_s = SupplierStock(
                                        product=p,
                                        supplier=s,
                                        code=product_d['code'],
                                        amount_available=product_d['units_minimum_amount'],
                                        #FIXME: django.core.exceptions.ValidationError: [u'This value must be a decimal number.']
                                        #FIXME: raise TypeError("Cannot convert %r to Decimal" % value)

                                        price=decimal.Decimal(self._avoid_empty(product_d['price'], 0.0)),
                                        #units_per_box=self._get_pretty(product_d['units_per_box'], STEP),
                                        #detail_minimum_amount=self._get_pretty(product_d['detail_minimum_amount'], STEP),
                                        #detail_step=self._get_pretty(product_d['detail_step'], STEP),
                                    )
                                    #s_s.save()


#    price = CurrencyField(verbose_name=_("price"))
#    code = models.CharField(verbose_name=_("code"), max_length=128, null=True, blank=True, help_text=_("Product 
#    amount_available = models.PositiveIntegerField(verbose_name=_("availability"), default=ALWAYS_AVAILABLE)
#    units_minimum_amount = models.PositiveIntegerField(default=1, verbose_name = _('units minimum amount'))
#    units_per_box = PrettyDecimalField(default=1, max_digits=5, decimal_places=2
#    detail_minimum_amount = PrettyDecimalField(default=1, verbose_name = _('detail minimum amount'),
#    detail_step = PrettyDecimalField(null=True, blank=True, default=1


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

    def _manage_multiple_duplicates(self, qs, display_attrs):

        model_verbose_plural = qs.model._meta.verbose_name_plural

        log.info(u"FOUND MANY DUPLICATES FOR %s: %s" % (
            model_verbose_plural,
            "\n".join([str(t) for t in qs.values_list(*display_attrs)])
        ))

        # 3 options: 
        # a. one instance of the querySet if the one that we need
        # b. same as "a." but overwrite info with new info
        # c. create another model instance

        raise NotImplementedError("cannot merge many %s" % model_verbose_plural)

    def _update_contacts(self, pers, d):
        """Process contacts of bound person."""

        emails = map(lambda x : x[0], pers.contacts.filter(flavour="EMAIL").values_list('value'))
        ans = "N"
        if d['email'] not in emails:
            ans = raw_input("Email %s not found for person %s. Found emails %s. Add it [y/N]?" % (d['email'], pers, emails))
            if ans == "Y":
                c_email = Contact.objects.create(flavour="EMAIL", value=d['email'])
            pers.contacts.add(c_email)
                
        return pers.contacts
        
    def _update_place(self, pers, d):
        """Process place already bound to person."""
        place = pers.address
        ans = "N"
        if place:
            ans = raw_input("Found address %s for person %s. Overwrite with new info %s [y/N]?" % \
                (place, pers, "city=%s address=%s name=''" % (d['city'], d.get('address','')))
            )
        else:
            place = Place()
            ans = "Y"

        if ans.upper() == "Y":
            place.city = d['city']
            place.address = d.get('address','')
            place.name = ''

        place.save()
        return place
        
    def _get_or_create_contacts(self, d):
        """Create contacts. Fields:
        * email: **required**
        * phone: optional
        """

        email = d['email'] or settings.JUNK_EMAIL
        try:
            c_email, created = Contact.objects.get_or_create(flavour="EMAIL", value=email)
        except Contact.MultipleObjectsReturned:
            
            contacts = Contact.objects.filter(flavour="EMAIL", value=email)
            try:
                ans = self._manage_multiple_duplicates(contacts, ('value', 'person', 'gas', 'supplier'))
            except NotImplementedError:
                #FIXME: create a new email contact entry
                c_email = Contact.objects.create(flavour="EMAIL", value=email)
            
        c_email.save()
        log.debug("CREATED EMAIL CONTACT %s" % c_email)
        print "CREATED EMAIL CONTACT %s" % (c_email)

        rv = [c_email]

        if d.has_key('phone'):
            c_phone, created = Contact.objects.get_or_create(flavour="PHONE", value=d['phone'])
            c_phone.save()
            rv.append(c_phone)
            log.debug("CREATED PHONE CONTACT %s" % c_email)
            print "CREATED PHONE CONTACT %s" % (c_email)

        return rv

    def _get_or_create_place(self, d):
        """Create place. Fields:
        * city: **required**
        * address: optional
        """

        kw = {
            'city' : d['city'],
            'address' : d.get('address',''),
            'name' : '',
        }

        pl, created = Place.objects.get_or_create(**kw)
        pl.save()
        if created:
            #UnicodeEncodeError: 'ascii' codec can't encode character u'\xe0' in position 21: ordinal not in range(128)
            #log.debug((u"CREATED PLACE %s" % pl).decode(ENCODING))
            print "CREATED PLACE %s" % (pl)
        return pl

    def _get_or_create_person(self, d, contacts, place):

        kw = {
            'name' : d['name'],
            'surname' : d['surname'],
        }

        # Person
        pers, created = Person.objects.get_or_create(**kw)

        if created:
            log.info(("CREATED PERSON %s" % pers).decode(ENCODING))
            if d.get('display_name'):
                pers.display_name = d['display_name']

            # Upload image
            if d.get('image'):

                log.info(("Setting image %s for person %s" % (d['image'], pers)).decode(ENCODING))
                f = File(file(d['image'], "rb"))
                pers.avatar = f

            pers.address = place
            pers.save()
            pers.contact_set.add(*contacts)

        else:
            pers = self._update_person(pers, d, contacts, place)

        pers.save()
        return pers

    def _get_certification(self, d):
        return CERTIFICATION
        #FIXME: TypeError: 'certifications' is an invalid keyword argument for this function
        log.info(pprint("AAAAAAAAAA  Certification"))
        rv = [4]
        if not d.has_key('certification'):
            return rv
        cert = d['certification']
        try:
            if not cert:
                return rv
            log.info(pprint("Certification (%s)" % (cert)))
            certs = Certification.objects.filter(symbol=cert)
            if certs:
                x = ", ".join(map(lambda x: x[0], certs.values_list('pk')))
                return [x]
            else:
                return rv

        except TypeError, e:
            log.info(pprint("TypeError get_certification (%s) --> %s" % (cert, e.message)))
            return rv
        except Certification.DoesNotExist, e:
            log.info(pprint("error get_certification (%s) --> %s" % (cert, e.message)))
            return rv

    def _avoid_empty(self, val_d, default):
        if not val_d or val_d =='' :
            return default

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

    def _get_pretty(self, val_d, default):
        #PrettyDecimalField
        #FIXME: django.core.exceptions.ValidationError: [u'This value must be a decimal number.']
        log.info(pprint("error params get_step (%s) --> %s----" % (val_d, default)))
        if not val_d or val_d == '' :
            return default
        try:
            #x=decimal.Decimal(val_d)
            #FOR TEST ONLY
            x=int(val_d)
        except:
            return default
        else:
            log.info(pprint("error get_step (%s) --> %s----" % (val_d, x)))
            return x
