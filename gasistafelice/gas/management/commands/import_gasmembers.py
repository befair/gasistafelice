
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

ENCODING = "iso-8859-1"

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
        m = CSVManager(fieldnames=fieldnames, delimiter=delimiter, encoding=ENCODING)
        data = m.read(csvdata)
        log.debug(pprint(m.read(csvdata)))

        # Data prepared

        g = GAS.objects.get(pk=gas_pk)
        g.config.auto_populate_products = True
        g.config.save()

        # STEP 2: process data and create instances
        with transaction.commit_on_success():
            for d in data:
                log.info("#### ---- start new user import... ----####")
                try:
                    user, updated = self._get_or_create_user(d)
                    try:
                        pers = user.person
                    except Person.DoesNotExist:
                        contacts = self._get_or_create_contacts(d)
                        place = self._get_or_create_place(d)
                        pers = self._get_or_create_person(d, contacts, place)
                        pers.user = user
                        pers.save()
                    else:
                        # This is a user of an already created person
                        log.info(("PERSON %s ALREADY EXISTENT" % user.person).decode(ENCODING)) 
                        if updated:
                            log.debug("UPDATE PERSON DETAILS")

                            contacts = self._update_contacts(user.person, d)
                            place = self._update_place(user.person, d)
                            pers = self._update_person(user.person, d, contacts, place, force=True)
                        else:
                            log.debug("SKIP IT")


                except KeyError, e:
                    if e.message not in self.allowed_keys:
                        raise CommandError("Invalid key '%s' provided. Allowed keys in python template are: %s" % (e.message, self.allowed_keys))
                    else:
                        raise CommandError("Key '%s' is REQUIRED." % e.message)

                gm, created = GASMember.objects.get_or_create(person=pers, gas=g)
                gm.save()
                log.info(("CREATED GASMEMBER %s" % gm).decode(ENCODING)) 
        return 0

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
            log.debug((u"CREATED PLACE %s" % pl).decode(ENCODING))

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

    def _update_person(self, pers, d, contacts, place, force=False):

        ans = "N"
        if force:
            ans = "Y"

        if pers.address != place:
            if not force:
                ans = raw_input("Found address %s for person %s. Overwrite with new address %s [y/N]?" % (pers.address, pers, place))
            if ans.upper() == "Y":
                pers.address = place

        if d.get('display_name'):
            if pers.display_name != d['display_name']:
                if not force:
                    ans = raw_input("Found display_name %s for person %s. Overwrite with new display_name %s [y/N]?" % (pers.address, pers, d['display_name']))
                if ans.upper() == "Y":
                    pers.display_name = d['display_name']

        # Upload image
        if not pers.avatar and d.get('image'):

            log.info(("Setting image %s for person %s" % (d['image'], pers)).decode(ENCODING))
            f = File(file(d['image'], "rb"))
            pers.avatar = f

        log.debug(("FOUND PERSON %s" % pers).decode(ENCODING))

        pers.name = d['name'].capitalize()
        pers.surname = d['surname'].capitalize()
        pers.save()
        return pers

    def _get_or_create_user(self, d):

        base_username = d.get('username') or d['name'].replace(' ','').lower()
        ans = ""
        updated = False

        users = User.objects.filter(email=d['email'])

        if users.count() > 1:

            ans = self._manage_multiple_duplicates(users, ('id','first_name', 'last_name', 'username', 'email'))

            # TODO TODO TODO

        elif users.count() == 1:
            
            user = users[0]
            log.info("FOUND USER WITH EMAIL %s: %s" % (
                d['email'], 
                "name=%s surname=%s username=%s" % (user.first_name, user.last_name, user.username)
            ))

            log.info("USER TO BE ADDED: name=%s surname=%s username=%s" % (d['name'], d['surname'], base_username))

            ans = "A"
            if user.username == base_username:
                log.info("Usernames match. Assuming person, contacts, and place info unchanged")
            else:
                msg = "Usernames don't match"
                ans = raw_input("%s. What should I do?\na. Keep current user as is\nb. Overwrite current user with new info\nc. Create a new user\n[A/b/c] ?" % msg)
                ans = ans.upper()

            if ans == "C":
                user = User(username=base_username, email=d['email'])

            elif ans == "B":
                user.first_name = d['name'].capitalize()
                user.last_name = d['surname'].capitalize()
                if User.objects.filter(username=base_username).count():
                    log.warning("CANNOT update username because it is already used")
                else:
                    user.username = base_username
                updated = True
        else:
            user = User(username=base_username, email=d['email'])
            user.first_name = d['name'].capitalize()
            user.last_name = d['surname'].capitalize()


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

                
        user.save()

        return user, updated

