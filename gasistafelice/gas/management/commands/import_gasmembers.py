
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError, transaction
from django.core.files import File

from django.contrib.auth.models import User
from gasistafelice.lib.csvmanager import CSVManager
from gasistafelice.lib import get_params_from_template
from gasistafelice.gas.models import GAS, GASMember
from gasistafelice.base.models import Place, Person, Contact

from pprint import pprint
import logging

log = logging.getLogger(__name__)
if settings.LOG_FILE:

    if not log.handlers:
        log.setLevel( logging.INFO )
        hdlr = logging.FileHandler(settings.LOG_FILE)
        hdlr.setFormatter( logging.Formatter('%(asctime)s %(levelname)s %(message)s') )
        log.addHandler(hdlr)


class Command(BaseCommand):
    args = "<gas_pk> <csv_file> [delimiter] [python_template]"
    allowed_keys = ['name','surname','email','city','image','address','display_name','phone']
    help = """Import gasmembers from csv file. Attributes allowed in python template are:

    """ + ",".join(allowed_keys) + """.

    """

    def handle(self, *args, **options):
        
        try:
            gas_pk = int(args[0])
            csv_filename = args[1]
        except:
            raise CommandError("Usage import_gasmembers: %s" % (self.args))

        if len(args) > 2:
            delimiter = args[2]
        else:
            delimiter = ";"

        if len(args) == 4:
            tmpl = args[3]
        else:
            tmpl = "%(name)s %(surname)s %(email)s %(city)s"

        # STEP 0: prepare data in dicts
        f = file(csv_filename, "rb")
        csvdata = f.read()
        f.close()

        fieldnames = get_params_from_template(tmpl)
        m = CSVManager(fieldnames=fieldnames, delimiter=delimiter)
        data = m.read(csvdata)
        log.debug(pprint(m.read(csvdata)))

        # Data prepared

        g = GAS.objects.get(pk=gas_pk)
        g.config.auto_populate_products = True
        g.config.save()

        # STEP 2: process data and create instances
        with transaction.commit_on_success():
            for d in data:
                try:
                    user = self._get_or_create_user(d)
                    try:
                        assert user.person
                        # This is a user of an already created person
                        log.info(("PERSON %s ALREADY EXISTENT. SKIP IT" % user.person).encode('utf-8')) 
                    except Person.DoesNotExist:
                        contacts = self._get_or_create_contacts(d)
                        place = self._get_or_create_place(d)
                        pers = self._get_or_create_person(d, contacts, place)
                        pers.user = user
                        pers.save()

                except KeyError, e:
                    if e.message not in self.allowed_keys:
                        raise CommandError("Invalid key '%s' provided. Allowed keys in python template are: %s" % (e.message, self.allowed_keys))
                    else:
                        raise CommandError("Key '%s' is REQUIRED." % e.message)

                gm, created = GASMember.objects.get_or_create(person=pers, gas=g)
                gm.save()
                log.info(("CREATED GASMEMBER %s" % gm).encode('utf-8')) 
        return 0

    def _get_or_create_contacts(self, d):
        """Create contacts. Fields:
        * email: **required**
        * phone: optional
        """

        c_email, created = Contact.objects.get_or_create(flavour="EMAIL", value=d['email'])
        c_email.save()
        log.debug("CREATED EMAIL CONTACT %s" % c_email)

        rv = [c_email]

        if d.has_key('phone'):
            c_phone, created = Contact.objects.get_or_create(flavour="PHONE", value=d['phone'])
            c_phone.save()
            rv.append(c_phone)
            log.debug("CREATED PHONE CONTACT %s" % c_email)

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
            log.debug((u"CREATED PLACE %s" % pl).encode('utf-8'))

        return pl

    def _get_or_create_person(self, d, contacts, place):

        kw = {
            'name' : d['name'],
            'surname' : d['surname'],
        }

        # Person
        pers, created = Person.objects.get_or_create(**kw)

        if d.has_key('display_name'):
            pers.display_name = d['display_name']

        if created:
            log.info(("CREATED PERSON %s" % pers).encode('utf-8'))
        else:
            if pers.address:
                ans = raw_input("Found address %s for person %s. Overwrite [y/N]?" % (pers.address, pers))
                if ans.upper() == "Y":
                    pers.address = place

            log.debug(("FOUND PERSON %s" % pers).encode('utf-8'))

        # Upload image
        if not pers.avatar and d.has_key('image'):

            log.info(("Setting image %s for person %s" % (d['image'], pers)).encode('utf-8'))
            f = File(file(d['image'], "rb"))
            pers.avatar = f

        pers.save()
        pers.contact_set.add(*contacts)
        pers.save()

        return pers

    def _get_or_create_user(self, d):

        base_username = d['name'].replace(' ','').lower()
        ans = "Y"
        try:
            user = User.objects.get(username=base_username, email=d['email'])
        except User.DoesNotExist:
            user = User(username=base_username, email=d['email'])
        else:
            pers = user.person
            if (pers.name != user.first_name) or (pers.surname != user.last_name):
                tmp_d = user.__dict__
                tmp_d.update({
                    'new_name' : d['name'],
                    'new_surname' : d['surname'],
                })
                
                ans = raw_input("Found user with name=%(first_name)s, surname=%(last_name)s \
                        Overwrite with name=%(new_name)s, surname=%(new_surname)s. Overwrite [y/N]?" % tmp_d
                )


        # Process only if we are creating a new user
        c = 1
        while not user.pk:
            try:
                sid = transaction.savepoint()
                user.save()
                transaction.savepoint_commit(sid)
            except IntegrityError:
                transaction.savepoint_rollback(sid)
                user.username = "%s%s" % ( base_username, c)
                c += 1
            else:
                user.set_password("default")
                user.is_active=False
                user.save()
                log.info("CREATED USER %s" % user) 

        if ans == "Y":
            user.first_name = d['name'].capitalize()
            user.last_name = d['surname'].capitalize()
                
        user.save()

        return user

