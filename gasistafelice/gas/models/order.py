"""Models related to Order management (including state machine)."""

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage

# Some template stuff needed for template rendering
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO
from django.utils.encoding import smart_unicode
# End
from workflows.models import Workflow, Transition
from workflows.utils  import set_initial_state
from gasistafelice.base.workflows_utils import get_workflow, set_workflow, get_state, do_transition, get_allowed_transitions
#from history.models import HistoricalRecords

from gasistafelice.base.models import PermissionResource, Place, DefaultTransition

from gasistafelice.base import validators

from gasistafelice.lib.fields.models import CurrencyField, PrettyDecimalField
from gasistafelice.lib.fields import display
from gasistafelice.lib import ClassProperty, unordered_uniq
from gasistafelice.lib.djangolib import queryset_from_iterable
from gasistafelice.supplier.models import Supplier
from gasistafelice.gas.models.base import GASMember, GASSupplierSolidalPact, GASSupplierStock
from gasistafelice.gas.managers import AppointmentManager, OrderManager
from gasistafelice.gas import signals
from gasistafelice.base.models import Person
from gasistafelice.consts import *
from gasistafelice.consts import FAKE_WITHDRAWN_AMOUNT
from gasistafelice.gas.workflow_data import STATUS_PREPARED, STATUS_OPEN
from gasistafelice.gas.workflow_data import STATUS_CLOSED, STATUS_UNPAID
from gasistafelice.gas.workflow_data import STATUS_ARCHIVED, STATUS_CANCELED

from gasistafelice.gas.workflow_data import TRANSITION_OPEN, TRANSITION_CLOSE, TRANSITION_CLOSE_EMAIL
from gasistafelice.gas.workflow_data import TRANSITION_ARCHIVE, TRANSITION_UNPAID, TRANSITION_CANCEL


from gasistafelice.utils import long_date, medium_date

from flexi_auth.models import ParamRole
from flexi_auth.utils import register_parametric_role
from flexi_auth.exceptions import WrongPermissionCheck

from django.conf import settings

from workflows.utils import do_transition
from datetime import datetime, timedelta
import logging, reversion

log = logging.getLogger(__name__)

#from django.utils.encoding import force_unicode
import copy, logging
log = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# Some stuff needed for translation

# NOTE LF: put some string to translate here... I don't know
# why makemessages don't find them
some_string_to_translate__ = (
    _("open: %(date_start)s"),
    _(" - close: %(date_end)s"),
    _("close: %(date_end)s"),
    _("close: unset"),
    _(" --> delivery: %(date_delivery)s"),
    _("to be delivered: %(date_delivery)s  --> to pay"),
    _("delivered: %(date_delivery)s --> to pay"),
    _("archived: %(date_delivery)s"),
    _("canceled: %(date_delivery)s"),
    _("Ord. %(order_num)s %(pact)s - %(state)s")
)

trans_state_d = {
    'Open' : 'Aperto',
    'Close': 'Chiuso',
    'Closed': 'Chiuso',
    'Archived' : 'Archiviato',
    'Prepared' : 'Preparato',
    'Unpaid' : 'Insoluto',
    'Canceled' : 'Annullato',
}

OF = _('of')
AT = _('at')
ON = _('on')
FROM = _('from')
TO = _('to')

#-------------------------------------------------------------------------------

class GASSupplierOrder(models.Model, PermissionResource):
    """An order issued by a GAS to a Supplier.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineFornitore>`__ for details (ITA only).

    * current_state is a meaningful parameter for order status from workflow system
    * gasstock_set references specified products available for the specific order \
      (they can be a subset of all available products from that Supplier for the order);

    """

    pact = models.ForeignKey(GASSupplierSolidalPact, related_name="order_set",verbose_name=_('pact'))
    datetime_start = models.DateTimeField(verbose_name=_('date open'),
        default=datetime.now, help_text=_("when the order will be opened")
    )
    datetime_end = models.DateTimeField(verbose_name=_('date close'),
        help_text=_("when the order will be closed"), null=True, blank=True
    )
    # minimum economic amount for the GASSupplierOrder to be accepted by the Supplier
    order_minimum_amount = CurrencyField(verbose_name=_('Minimum amount'),
        null=True, blank=True
    )
    # Where and when Delivery occurs
    # FUTURE TODO: must be ManyToManyField
    delivery = models.ForeignKey('Delivery',
        verbose_name=_('Delivery'), related_name="order_set", null=True, blank=True
    )

    # Where and when Withdrawal occurs
    # FUTURE TODO: must be ManyToManyField
    withdrawal = models.ForeignKey('Withdrawal',
        verbose_name=_('Withdrawal'), related_name="order_set", null=True, blank=True
    )

    # Delivery cost. To be set after delivery has happened
    delivery_cost = CurrencyField(verbose_name=_('Delivery cost'), null=True, blank=True)

    gasstock_set = models.ManyToManyField(GASSupplierStock,
        verbose_name=_('GAS supplier stock'),
        help_text=_("products available for the order"),
        blank=True, through='GASSupplierOrderProduct'
    )

    referrer_person = models.ForeignKey(Person, null=True, blank=True,
        related_name="order_set", verbose_name=_("order referrer"),
        #KO it passes person pk: validators=[validators.attr_user_is_set]
    )

    delivery_referrer_person = models.ForeignKey(Person,
        null=True, related_name="delivery_for_order_set", blank=True,
        verbose_name=_("delivery referrer"),
        #KO it passes person pk: validators=[validators.attr_user_is_set]
    )
    withdrawal_referrer_person = models.ForeignKey(Person,
        null=True, related_name="withdrawal_for_order_set", blank=True,
        verbose_name=_("withdrawal referrer"),
        #KO it passes person pk: validators=[validators.attr_user_is_set]
    )

    group_id = models.PositiveIntegerField(verbose_name=_('Order group'),
        null=True, blank=True,
        help_text=_("If not null this order is aggregate with orders from other GAS")
    )

    invoice_amount = CurrencyField(null=True, blank=True, verbose_name=_("invoice amount"))
    invoice_note = models.TextField(blank=True, verbose_name=_("invoice number"))

    root_plan = models.ForeignKey('GASSupplierOrder', null=True, blank=True, default=None,
        help_text=_("Order was generated by another order"), verbose_name=_("planned order"))

    objects = OrderManager()

    #WAS: history = HistoricalRecords()

    class Meta:
        verbose_name = _('order issued to supplier')
        verbose_name_plural = _('orders issued to supplier')
        ordering = ('datetime_end', 'datetime_start')
        app_label = 'gas'

    def __init__(self, *args, **kw):
        super(GASSupplierOrder, self).__init__(*args, **kw)

    @property
    def state_info(self):

        d = {}

        d['date_start'] = medium_date(self.datetime_start)

        if self.datetime_end is not None:
            d['date_end'] = medium_date(self.datetime_end)
        d['date_delivery'] = ""
        if self.delivery:
            if self.delivery.date:
                d['date_delivery'] = medium_date(self.delivery.date)

        state = ""
        date_info = ""
        if self.current_state:
            state = self.current_state.name
            date_info = "("
            if state == STATUS_PREPARED:
                date_info += ugettext("open: %(date_start)s")
                if self.datetime_end:
                    date_info += ugettext(" - close: %(date_end)s")

            elif state == STATUS_OPEN:

                if self.datetime_end:
                    date_info += ugettext("close: %(date_end)s")
                else:
                    date_info += ugettext("close: unset")

                if d['date_delivery']:
                    date_info += ugettext(" --> delivery: %(date_delivery)s")

            elif state == STATUS_CLOSED:
#                if self.datetime_end:
#                    date_info += ugettext("Closed: %(date_end)s")

                if d['date_delivery']:
                    date_info += ugettext("to be delivered: %(date_delivery)s  --> to pay")


            elif state == STATUS_UNPAID:
                if d['date_delivery']:
                    date_info += ugettext("delivered: %(date_delivery)s --> to pay")

            elif state == STATUS_ARCHIVED:
                if d['date_delivery']:
                    date_info += ugettext("archived: %(date_delivery)s")

            elif state == STATUS_CANCELED:
                if d['date_delivery']:
                    date_info += ugettext("canceled: %(date_delivery)s")

            else:
                date_info += "TODO ?(%s)" % state
            date_info += ")"

        date_info = date_info % d

        state = trans_state_d.get(state, state)
        state += " " + date_info
        return state

    @property
    def common_name(self):
        cn = ugettext("Ord. %(order_num)s %(pact)s") % {
            'order_num' : self.pk,
            'pact' : self.pact,
        }
        return cn

    def __unicode__(self):

        state = self.state_info

        ref = self.referrer_person

        if ref:
            ref = " ref: %s " % ref
        elif self.referrer_person:
            ref = " ref: %s " % self.referrer_person
        else:
            ref = ""

        rv = "%(common_name)s - %(state)s" % {
            'common_name' : self.common_name,
            'state' : state,
            'ref' : ref
        }

        if self.group_id:
            rv += " --> InterGAS. %s" % (self.group_id)
        #if settings.DEBUG:
        #    rv += " [%s]" % self.pk
        return rv


    @property
    def report_name(self):
        rep_date = medium_date(self.datetime_end)
        if self.delivery:
            if self.delivery.date:
                rep_date = medium_date(self.delivery.date)
        return u"Ord.%s %s %s %s" % (self.pk, OF, rep_date, self.supplier.subject_name)

    @property
    def display_totals(self):
        """Show totals expected, actual and curtailed"""

        return ugettext(u"Expected: %(fam)s euro --> Actual: %(fatt)s euro --> Curtailed: %(eco)s euro") % {
            'fam'    : "%.2f" % round(self.tot_price, 2)
            , 'fatt' : "%.2f" % round(self.invoice_amount or 0, 2)
            , 'eco'  : "%.2f" % round(self.tot_curtail, 2)
        }

    def do_transition(self, transition, user):
        super(GASSupplierOrder, self).do_transition(transition, user)
        if self.is_active():
            log.debug("Order %d OPENED by transition=%s: settings default gasstock set" % (
                self.pk, transition.name
            ))
            self.set_default_gasstock_set()
        signals.order_state_update.send(sender=self, transition=transition)

    def open_if_needed(self, sendemail=False, issuer=None):
        """Check datetime_start and open order if needed."""
        if self.gas.config.is_suspended:
            log.debug("open_if_needed: GAS(%s) suspended" % (self.gas))
            return

        if self.datetime_start <= datetime.now():

            # Act as superuser
            user = User.objects.get(username=settings.INIT_OPTIONS['su_username'])
            t_name = TRANSITION_OPEN
            t = Transition.objects.get(name__iexact=t_name, workflow=self.workflow)

            if t in get_allowed_transitions(self, user):
                log.debug("Do %s transition. datetime_start is %s" % (t, self.datetime_start))

                self.do_transition(t, user)

                #TODO Send email will be done with notice_days_before_order_close

    def get_absolute_url_order_page_for_user(self, user):

        gasmembers = user.person.gasmembers.filter(gas=self.gas)
        if gasmembers.count():
            absolute_url = gasmembers[0].get_absolute_url_page()
        else:
            absolute_url = None

        return absolute_url

    def close(self, force_email=False, issuer=None):
        """Close an order."""

        # COMMENT fero: I don't understand the followind check...
        # COMMENT fero: IMHO this should raise ClosingOrderAlreadyClosedException

        # Control is not yet in closed state due to InterGAS Order generation
        # Only in the case taht we operate the InterGAS management 1)
        if self.is_closed():
            log.debug("close_if_needed: GAS(%s) already closed" % (self.gas))
            return

        # Act as superuser
        user = User.objects.get(username=settings.INIT_OPTIONS['su_username'])
        t_name = TRANSITION_CLOSE
        t = Transition.objects.get(name__iexact=t_name, workflow=self.workflow)

        if t in get_allowed_transitions(self, user):
            self.do_transition(t, user)
            return True
        else:
            return False

    def close_if_needed(self, force_email=False, issuer=None):
        """Check for datetime_end and close order if needed. if GAS is running"""
        if self.gas.config.is_suspended:
            log.debug("close_if_needed: GAS(%s) suspended" % (self.gas))
            #TODO: raise ClosingOrderWhileGASSuspendedException
            return

        if self.datetime_end:
            if self.datetime_end <= datetime.now():

                #InterGAS.
                cc_intergas_people = Person.objects.none()

                #COMMENT domthu: we have to possibility to manage it
                # 1) send one unique email with all GAS's reports and the cumulative report
                #    attached to the email [CONFIRMED CHOICE domthu+fero]
                # 2) send x emails as GAS number participants. each email will have the own GAS's
                #    report with the cumulative report attached to the email

                if self.is_intergas:

                    # Close all related InterGAS orders without sending email
                    # Collect all cc to be joined to the single sended email
                    for order in self.get_complementary_intergas_orders():
                        cc_intergas_people |= order.pact.referrers_people
                        order.close(False, None)

                is_closed = self.close(force_email, issuer)

                if is_closed and \
                    (self.pact.send_email_on_order_close or force_email):

                        # NOTE domthu: self.pact.send_email_on_order_close default is
                        # specified in self.gas.config.send_email_on_order_close

                        cc_people = self.pact.referrers_people | cc_intergas_people
                        cc = map(lambda x : x.preferred_email_address, cc_people)
                        self.send_email_to_supplier(cc, ugettext('Automatic send on close'))

    def get_valid_name(self):
        from django.template.defaultfilters import slugify
        from django.utils.encoding import smart_str
        n = str(self.pk) + '_'
        n += smart_str(slugify(self.pact.supplier.name).replace('-', '_'))
        #n += '_{0:%Y%m%d}'.format(self.delivery.date)
        #TODO: Auto create appointment for delivery date (Discuss about order type implementation)
        if self.delivery and self.delivery.date:
            n += '_{0:%Y%m%d}'.format(self.delivery.date)
        else:
            n += '_{0:%Y%m%d}'.format(datetime.now())
        return n
        #return self.pact.supplier.name.replace('-', '_').replace(' ', '_')

    #-- Contacts --#

    @property
    def contacts(self):
        return Contact.objects.filter(person__in=self.info_people)

    @property
    def info_people(self):
        return self.pact.info_people

    #-------------------------------------------------------------------------------#
    # Model Archive API

    def is_prepared(self):
        """
        Return `True` if the GAS supplier order is prepared; `False` otherwise.
        """
        #return self in GASSupplierOrder.objects.prepared()
        return self.current_state.name == STATUS_PREPARED

    def is_active(self):
        """
        Return `True` if the GAS supplier order is to be considered as 'active'; `False` otherwise.
        """
        #return self in GASSupplierOrder.objects.open()
        return self.current_state.name == STATUS_OPEN

    def is_archived(self):
        """
        Return `True` if the GAS supplier order is to be considered as 'archived'; `False` otherwise.
        """
        return self.current_state.name == STATUS_ARCHIVED

    def is_closed(self):
        """
        Return `True` if the GAS supplier order is closed; `False` otherwise.
        """
        return self.current_state.name == STATUS_CLOSED

    def is_unpaid(self):
        """
        Return `True` if the GAS supplier order is closed but producer is not payed; `False` otherwise.
        """
        return self.current_state.name == STATUS_UNPAID

    def is_canceled(self):
        """
        Return `True` if the GAS supplier order is canceled; `False` otherwise.
        """
        return self.current_state.name == STATUS_CANCELED


    #-------------------------------------------------------------------------------#

    @property
    def referrers(self):
        """Return all users being referrers for this order.

        Referrers for a pact include people bound to the specific path,
        or, if not specified, all gas referrers.

        This way we can manage two cases:
        * Pacts that have specific operators
        * Pacts who inherits operators from GAS and so involve all gas referrers

        Remember that in Gasista Felice referrer == operator
        (and info_people is for communicative referrers)
        """

        order_refs = self.pact.referrers
        if not order_refs:
            order_refs = self.pact.gas.referrers

        # FIXED: 'NoneType' object has no attribute 'user'.
        # COMMENT: validator `attr_user_is_set` for `referrer_*` fields.
        # COMMENT: Cannot be real for any kind of referrer. But model permits this.

        # QUESTION: are we sure that this is a FIXME? In this case, would it be simpler
        # to perform this check as you have done here, and let users specify
        # a person as an order referrer even if it is not a user in the system ?
        # ANSWER: discussed even with Orlando. No-sense here informational person.
        # So Matteo will apply "TO FIX" described up here.
        if self.referrer_person and self.referrer_person.user:
            order_refs |= User.objects.filter(pk=self.referrer_person.user.pk)

        return order_refs

    @property
    def supplier_referrers_people(self):
        prs = Person.objects.none()
        if self.referrers:
            prs = Person.objects.filter(user__in=self.referrers)
        return prs

    @property
    def cash_referrers(self):
        return self.pact.gas.cash_referrers

    #-------------------------------------------------------------------------------#

    def set_default_gasstock_set(self):
        '''
        A helper function associating a default set of products to a GASSupplierOrder.

        At this time of execution we cannot use self.gasstock_set because we are building it.

        At this time of the software development every Product bound to pact,
        and so to the GAS, are included in list of orderable products for this order.

        In future, we could have the ability to choose products one-by-one, but this is not
        our case now, so don't care about it.
        '''

#COMMENT LF - TO BE REMOVED
#        if not self.pact.gas.config.auto_populate_products:
#            log.debug(ugettext("GAS is not configured to auto populate all products. You have to select every product you want to put into the order"))
#            return

        gasstocks = GASSupplierStock.objects.filter(pact=self.pact, enabled=True)
        for s in gasstocks:
            #maybe works the more intuitive...self.orderable_product_set.add( ???
            GASSupplierOrderProduct.objects.create(order=self,
                gasstock=s, initial_price=s.price, order_price=s.price,
                delivered_price=s.price
            )

    #--------------------------------------------------------------------------------

    def revert_order(self, force=False):
        """Can revert order to initial state.

        Meant to be used just for debug or recovery situations"""

        if not force:
            return

        self.gasstock_set.delete()
        set_initial_state(self)

    def add_product(self, s):
        '''
        A helper function to add product to a GASSupplierOrder.
        '''

        # We can retrieve GASSupplierOrderProduct bound to this order with
        # self.orderable_products but it is useful to use get_or_create
        gsop, created = GASSupplierOrderProduct.objects.get_or_create(order=self, gasstock=s, order_price=s.price, initial_price=s.price)
        if created:
            #log.debug('No GSOP found in order(%s) state(%s)' % (self.pk, self.current_state))
            gsop.order_price = s.price
            gsop.save()
        else:
            #log.debug('GSOP already present in order(%s) state(%s)' % (self.pk, self.current_state))
            if gsop.delivered_price != s.price:
                gsop.delivered_price = s.price
                gsop.save()

    def remove_product(self, s):
        '''
        A helper function to remove a product from a GASSupplierOrder.
        '''
        #TODO: Does workflows.utils have method state_in(tupple of state)
        #if (order.current_state == OPEN) | (order.current_state == CLOSED)

        try:
            gsop = self.orderable_products.get(gasstock=s)
            #log.debug('product %s found in order %s' % (s.stock, self.order))
        except GASSupplierOrderProduct.DoesNotExist:
            log.debug('No product found in order(%s) state(%s)' % (self.pk, self.current_state))

        else:
            #log.debug('product found in order(%s) state(%s)' % (self.pk, self.current_state))
            #Delete all GASMemberOrders done
            lst = gsop.gasmember_order_set.all()
            total = 0
            count = lst.count()
            for gmo in lst:
                total += gmo.ordered_price
                log.debug('Deleting gas member %s email %s: Unit price(%s) ordered quantity(%s) total price(%s) for product %s' % (gmo.purchaser, gmo.purchaser.email, gmo.ordered_price, gmo.ordered_amount, gmo.ordered_price, gmo.product, ))
                signals.gmo_product_erased.send(sender=gmo)
                gmo.delete()
            #log.debug('Deleted gas members orders (%s) for total of %s euro' % (count, total))
            gsop.delete()


    # Workflow management

    @property
    def current_state(self):
        return get_state(self)

    @property
    def localized_current_state(self):
        s = self.current_state.name
        return trans_state_d.get(s, s)

    @property
    def workflow(self):
        return get_workflow(self)

    @workflow.setter
    def workflow(self, value=None):
        raise AttributeError(ugettext("Workflow for specific GASSupplierOrder is not allowed. Just provide a default order workflow for your GAS"))

    def forward(self, user):
        """Apply default transition"""
        state = get_state(self)
        transition = DefaultTransition.objects.get(workflow=self.workflow, state=state).transition
        do_transition(self, transition, user)

    # -- Resource API --#

    @ClassProperty
    @classmethod
    def resource_type(cls):
        return "order"

    @property
    def parent(self):
        return self.pact

    @property
    def des(self):
        return self.gas.des

    @property
    def gas(self):
        """Return the GAS issuing this order."""
        return self.pact.gas

    @property
    def supplier(self):
        """Return the supplier this order is placed against."""
        return self.pact.supplier

    @property
    def suppliers(self):
        return Supplier.objects.filter(pk=self.supplier.pk)

    @property
    def orderable_products(self):
        return self.orderable_product_set.all()
    #ERROR: An unexpected error occurred while tokenizing input
    #The following traceback may be corrupted or invalid
    #The error message is: ('EOF in multi-line statement', (390, 0))

    @property
    def ordered_gasmembers(self):
        from django.db.models import Count, Sum
        #Do not use string formatting on raw queries!
        return GASMember.objects.raw("\
SELECT tmp.id AS id,  \
( SELECT SUM(gmo.ordered_price*gmo.ordered_amount) FROM \
gas_gasmemberorder AS gmo \
INNER JOIN gas_gassupplierorderproduct AS gsop \
ON gmo.ordered_product_id = gsop.id \
WHERE gsop.order_id = %s AND gmo.purchaser_id = tmp.id \
) AS sum_amount FROM gas_gasmember as tmp \
WHERE tmp.id IN ( SELECT gmo2.purchaser_id FROM gas_gasmemberorder as gmo2 \
INNER JOIN gas_gassupplierorderproduct AS gsop2 \
ON gmo2.ordered_product_id = gsop2.id \
WHERE gsop2.order_id = %s ) \
", [self.pk, self.pk])

    @property
    def ordered_gasmembers_sql(self):
        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute("SELECT id AS purchaser_id,  \
( SELECT SUM(gmo.ordered_price*gmo.ordered_amount) FROM \
gas_gasmemberorder AS gmo \
INNER JOIN gas_gassupplierorderproduct AS gsop \
ON gmo.ordered_product_id = gsop.id \
WHERE order_id = %s \
) AS sum_amount", [self.pk])
        #TODO: Add new field account_amounted
        #Field are retrieve from the Accounting system
        desc = cursor.description
        row = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]
        return row

    @property
    def ordered_products(self):
        return GASMemberOrder.objects.filter(ordered_product__in=self.orderable_products)

    @property
    def stocks(self):
        from gasistafelice.supplier.models import SupplierStock
        stocks_pk=map(lambda x: x[0], self.gasstock_set.values_list('stock'))
        return SupplierStock.objects.filter(pk__in=stocks_pk)

    @property
    def gasstocks(self):
        return self.gasstock_set.all()

    @property
    def gasmembers(self):
        return self.gas.gasmembers

    @property
    def orders(self):
        return GASSupplierOrder.objects.filter(pk=self.pk)

    @property
    def order(self):
        return self

    @property
    def purchasers(self):
        """
        The set of GAS members participating to this supplier order.
        """
        purchasers = [order.purchaser for order in self.member_orders]
        return queryset_from_iterable(GASMember, purchasers).distinct()

    @property
    def member_orders(self):
        """
        The queryset of GAS members' orders issued against this supplier order.
        """
        member_orders = GASMemberOrder.objects.filter(ordered_product__order=self)
        return member_orders

    @property
    def total_amount(self):
        """
        The total expense for this order, as resulting from the invoice.
        """
        amount = 0
        for order_product in self.orderable_products:
            price = order_product.delivered_price
            quantity = order_product.delivered_amount
            amount += price * quantity
        return amount

    @property
    def tot_price(self):
        tot = 0
        for gmo in self.ordered_products:
            tot += gmo.price_expected
        return tot

    @property
    def tot_amount(self):
        tot = 0
        if self.ordered_products:
            from django.db.models import Count, Sum
            qry = self.ordered_products.values('purchaser').annotate(sum_qta = Sum('ordered_amount')).order_by('purchaser').filter( is_confirmed = True)
            for agg_gmo in qry:
                tot += agg_gmo.sum_qta
        return tot

    @property
    def tot_gasmembers(self):
        tot = 0
        if self.ordered_products:
            from django.db.models import Count, Sum
            qry = self.ordered_products.values('purchaser').annotate(sum_qta = Sum('ordered_amount')).order_by('purchaser').filter( is_confirmed = True)
            tot = qry.count()
        return tot

    @property
    def tot_curtail(self):
        tot = 0
        accounted_amounts = self.gas.accounting.accounted_amount_by_gas_member(self)
        for member in accounted_amounts:
            tot += (member.accounted_amount or 0)
        return tot

    @property
    def payment(self):
        yet_payed, descr, date =self.gas.accounting.get_supplier_order_data(self)
        return yet_payed

    @property
    def payment_urn(self):
        mvt_urn = self.urn
        return mvt_urn

    def control_economic_state(self):

        # 1/3 control invoice receipt
        if not self.invoice_amount:
            return

        # 2/3 control members curtails
        accounted_amounts = self.gas.accounting.accounted_amount_by_gas_member(self)

        if not len(accounted_amounts):
            return

        purchasers = self.purchasers
        c_purch = purchasers.count()
        l_accounted = len(accounted_amounts)

        if c_purch > l_accounted:
            # LF: leave this check here, is faster than the next "fine tune check"
            return
        else:
            #LF: we have to check "number of accounted amounts among purchasers"
            #LF: in fact there may be new added families that need the following check.
            #LF: keep in mind that if a gasmember places an order,
            #LF: there must be a transaction even if it is of 0 cash amount

            n_added_families = 0
            for gm in accounted_amounts:
                if gm not in purchasers:
                    n_added_families += 1
                    if c_purch > (l_accounted - n_added_families):
                        return

        # 3/3 control accounting payment to supplier
        tx = self.gas.accounting.get_supplier_order_transaction(self)
        if tx:
            #change state to STATUS_ARCHIVED
            t_name = TRANSITION_ARCHIVE
        else:
            #change state to STATUS_UNPAID
            t_name = TRANSITION_UNPAID

        # Act as superuser
        user = User.objects.get(username=settings.INIT_OPTIONS['su_username'])
        t = Transition.objects.get(name__iexact=t_name, workflow=self.workflow)
        if t in get_allowed_transitions(self, user):
            self.do_transition(t, user)


    @property
    def insolutes(self):
        orders = GASSupplierOrder.objects.closed().filter(pact=self.pact) | \
            GASSupplierOrder.objects.unpaid().filter(pact=self.pact)
        return orders

    def clean(self):

        if self.referrer_person:
            validators.attr_user_is_set(self.referrer_person)

        if self.delivery_referrer_person:
            validators.attr_user_is_set(self.delivery_referrer_person)

        if self.withdrawal_referrer_person:
            validators.attr_user_is_set(self.withdrawal_referrer_person)

    def save(self, *args, **kw):
        self.full_clean()
        created = False

        if not self.pk:
            created = True
            if self.gas.config.use_withdrawal_place:

                # Create default withdrawal
                if self.datetime_end and not self.withdrawal:

                    #TODO: check gasconfig for weekday
                    w = Withdrawal(
                            date=self.datetime_end + timedelta(7),
                            place=self.gas.config.withdrawal_place
                    )
                    w.save()
                    self.withdrawal = w

        super(GASSupplierOrder, self).save(*args, **kw)

        #KO: 20111212 02:00 prepare reccurent plan for order.
        #KO:  because Do not create gasstock if order state is prepared
        #KO: if created:
        #KO:     self.set_default_gasstock_set()

    #-------------- Authorization API ---------------#

    # Table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        """Who can create a supplier order?

        In general:
            * GAS administrators
            * Referrers for the pact the order is placed against
        Cannot create order if resource related gas have no supplier_referrers.

        In depth we have to switch among multiple possible contexts

        If we are checking for a "unusual key" (not in ctx_keys_to_check),
        just return False, do not raise an exception.
        """

        allowed_users = User.objects.none()
        ctx_keys_to_check = set(('pact', 'gas', 'site', 'supplier'))
        ctx_keys = context.keys()

        if len(ctx_keys) > 1:
            raise WrongPermissionCheck('CREATE [only one key supported for context]', cls, context)

        k = ctx_keys[0]

        if k not in ctx_keys_to_check:
            # No user is allowed, just return False
            # (user is not in User empty querySet)
            # Do not raise an exception
            pass

        # Switch among possible different contexts

        elif k == 'pact':
            # pact context
            pact = context[k]
            if pact.gas.supplier_referrers.count():
                allowed_users = pact.gas.tech_referrers | pact.gas.supplier_referrers

        elif k == 'gas':
            # gas context
            gas = context[k]
            if gas.pacts.count() and gas.supplier_referrers.count():
                allowed_users = gas.tech_referrers | gas.supplier_referrers

        elif k == 'site':
            # des context
            des = context[k]
            if des.pacts.count():
                allowed_users = des.gas_tech_referrers | des.gas_supplier_referrers

        elif k == 'supplier':
            # supplier context
            # Every GAS REFERRER SUPPLIER or GAS REFERRER TECH of a GAS
            # who has a GASSupplierSolidalPact with this Supplier
            supplier = context[k]
            for pact in supplier.pacts:
                allowed_users |= pact.gas.supplier_referrers | pact.gas.tech_referrers

        return user in allowed_users

    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        if self.is_archived():
            allowed_users = []
        else:
            allowed_users = self.referrers | self.gas.tech_referrers | self.gas.supplier_referrers
        return user in allowed_users

    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can edit details of a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        allowed_users = self.referrers | self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    #-----------------------------------------------#

    def send_email(self, to, cc=[], more_info='', issued_by=None):

        if not isinstance(to, list):
            to = [to]

        log.debug('SENDING EMAIL: self=%s to=%s, cc=%s' % (self, to, cc))

        try:
            log.debug('self.gas.preferred_email_contacts %s ' % self.gas.preferred_email_contacts)
            sender = self.gas.preferred_email_contacts[0].value
        except IndexError as e:
            msg = ugettext("GAS cannot send email, because no preferred email for GAS specified")
            sender = settings.DEFAULT_FROM_EMAIL
            more_info += '%s --> %s' % (msg, sender)

        subject = u"[ORDINE] %(gas_id_in_des)s - %(ord)s" % {
            'gas_id_in_des' : self.gas.id_in_des,
            'ord' : self
        }

        message = u"In allegato l'ordine del GAS %(gas)s. " % { 'gas': self.gas }
        message += more_info
        #WAS: send_mail(subject, message, sender, recipients, fail_silently=False)

        to = unordered_uniq(to)
        cc = unordered_uniq(cc or [])
        email = EmailMessage(
            subject = subject,
            body = message,
            from_email = sender,
            to = to, cc = cc,
        )

        #FIXME: No handlers could be found for logger "xhtml2pdf"
        pdf_data = self.get_pdf_data(requested_by=issued_by)
        if not pdf_data:
            email.body += ugettext('We had some errors in report generation. Please contact %s') % settings.SUPPORT_EMAIL
        else:
            email.attach(
                u"%s.pdf" % self.get_valid_name(),
                pdf_data,
                'application/pdf'
            )

        # InterGAS, generate cumulative orders
        if self.is_intergas:

            log.debug("InterGAS report (%s)" % self.group_id)
            # Only in case we use InterGAs management 1)
            # Retrieve all others relative orders
            for order in self.get_complementary_intergas_orders():

                other_pdf_data = order.get_pdf_data(requested_by=issued_by)
                if not other_pdf_data:
                    email.body += ugettext('We had some errors in report generation. Please contact %s') % settings.SUPPORT_EMAIL
                    email.body += ugettext('For InterGAS => %s') % order
                else:
                    email.attach(
                        u"%s.pdf" % order.get_valid_name(),
                        other_pdf_data,
                        'application/pdf'
                    )

            # The cumulative order
            intergas_pdf_data = self.get_intergas_pdf_data(requested_by=issued_by)
            if not intergas_pdf_data:
                email.body += ugettext('We had some errors in report generation. Please contact %s') % settings.SUPPORT_EMAIL
            else:
                email.attach(
                    u"%s.pdf" % self.get_valid_name(),
                    intergas_pdf_data,
                    'application/pdf'
                )

        email.send()

        return

    def send_email_to_supplier(self, cc=[], more_info='', issued_by=None):
        supplier_email = self.supplier.preferred_email_address
        #Control if GAS and PACT are abilitate to send email
        if self.pact.is_suspended:
            log.debug("Unauthorized email for suspended producer %(o)s" % { 'o':self.pact })
        else:
            return self.send_email(
                [supplier_email],
                cc=cc, more_info=more_info,
                issued_by=issued_by
            )

    def render_as_html(self, requested_by=None):

        if not requested_by:
            requested_by = User.objects.get(username=settings.INIT_OPTIONS['su_username'])

        orderables_aggregate = self.orderable_products.filter(
            gasmember_order_set__ordered_amount__gt=0
        ).distinct().order_by('gasstock__stock__supplier_category__sorting')

        ordereds = self.ordered_products.order_by('purchaser__person__name',
            'purchaser__person__surname', 'purchaser__person',
            'ordered_product__gasstock__stock__supplier_category__sorting',
            'ordered_product__gasstock__stock__product__category__name'
        )

        fams, total_calc, subTotals, fam_count = self.__get_pdfrecords_families(ordereds)
        # if there are PDF PROBLEM try to print...
        # print("AAAAAA fams=%s total_calc=%s subTotals=%s" % (fams, total_calc, subTotals))
        context_dict = {
            'order' : self,
            'recProd' : self.__get_pdfrecords_products(orderables_aggregate),
            'prod_count' : orderables_aggregate.count(),
            'recFam' : fams,
            'fam_count' : fam_count,
            'subFam' : subTotals,
            'total_amount' : self.tot_price, #total da Model
            'total_calc' : total_calc, #total dal calcolato
            'have_note' : bool(self.allnotes.count() > 0),
            'user' : requested_by,
        }

        REPORT_TEMPLATE = "blocks/order_report/report.html"

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        return html

    def get_pdf_data(self, requested_by=None):
        """Return PDF raw content to be rendered somewhere (email, or http)"""

        html = self.render_as_html(requested_by=requested_by)
        result = StringIO.StringIO()
        #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1", "ignore")), result)
        pisadoc = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8", "ignore")), result)
        if not pisadoc.err:
            rv = result.getvalue()
        else:
            log.debug('Some problem while generate pdf err: %s' % pisadoc.err)
            rv = None
        return rv
    #MOD
    def get_html_data(self, requested_by=None):
        """Return HTML raw content to be rendered somewhere (email, or http)"""

        html = self.render_as_html(requested_by=requested_by)

        result = StringIO.StringIO(html.encode("utf-8", "ignore"))
        if html:
            rv = result
        else:
            # print "Some problem while generating html"
            rv = None
        return rv

    def __get_pdfrecords_families(self, querySet):
        """Return records of rendered table fields."""

        records = []
        # memorize family, total price and number of products
        subTotals = []
        fam_count = 0
        actualFamily = -1
        loadedFamily = -1
        rowFam = -1
        description = ""
        product = ""
        tot_fam = 0
        nProducts = 0
        tot_Ord = 0

        for el in querySet:
            rowFam = el.purchaser.pk
            if actualFamily == -1 or actualFamily != rowFam:
                if actualFamily != -1:
                    subTotals.append({
                       'family_id' : actualFamily,
                       'gasmember' : description,
                       'basket_price' : tot_fam,
                       'basket_products' : nProducts,
                    })
                    tot_fam = 0
                    nProducts = 0
                actualFamily = rowFam
                fam_count += 1
                description = smart_unicode(el.purchaser.person)
            product = smart_unicode(el.product)

            tot_fam += el.price_expected
            nProducts += 1
            tot_Ord += el.price_expected

            records.append({
               'product' : product,
               'price_ordered' : el.ordered_price,
               'price_delivered' : el.ordered_product.order_price,
               'price_changed' : el.has_changed,
               'amount' : el.ordered_amount,
               'tot_price' : el.price_expected,
               'family_id' : rowFam,
               'note' : el.note,
            })

        if actualFamily != -1 and tot_fam > 0:
            subTotals.append({
               'family_id' : actualFamily,
               'gasmember' : description,
               'basket_price' : tot_fam,
               'basket_products' : nProducts,
            })

        return records, tot_Ord, subTotals, fam_count

    def __get_pdfrecords_products(self, querySet):
        """Return records of rendered table fields."""

        records = []
        c = querySet.count()

        for el in querySet:
            if el.tot_price > 0:
                records.append({
                   'product' : el.gasstock,
                   'rep_price' : el.gasstock.report_price,
                   'price' : el.order_price,
                   'tot_gasmembers' : el.tot_gasmembers,
                   'tot_amount' : el.tot_amount,
                   'tot_price' : el.tot_price,
                })
        return records

    #-----------------------------------------------#
    # InterGAS

    @property
    def is_intergas(self):
        return bool(self.group_id)

    def get_complementary_intergas_orders(self):
        return self.get_intergas_orders().exclude(pk=self.pk)

    def get_intergas_orders(self):
        if self.is_intergas:
            return GASSupplierOrder.objects.filter(group_id=self.group_id)
        #FUTURE TODO: to be verified if it does not hits the QuerySet cache and to be optimized
        return GASSupplierOrder.objects.filter(pk=self.pk)

    def get_planned_orders(self):
        """Return planned orders"""
        qs = GASSupplierOrder.objects.none()
        for order in self.get_intergas_orders():
            qs |= GASSupplierOrder.objects.filter(
                pact=order.pact,
                datetime_start__gt = order.datetime_start
            )
        return qs

    def clone(self, reuse_delivery=False, reuse_withdrawal=False):
        """Clone an order. Keeping pact, while binding empty Delivery and Withdrawal.

        Useful for planning orders.
        """
        #WAS: GetNewOrder

        new_obj = copy.copy(self)
        if not reuse_withdrawal:
            new_obj.withdrawal = None
        if not reuse_delivery:
            new_obj.delivery = None

        new_obj.pk = None
        set_initial_state(new_obj)

        return new_obj

    def plan(self, n_items, frequency):
        """Plan the present order. Subtle optimization if InterGAS.

        Create n_items GASSupplierOrder with stable `frequecy`.

        This method must be invoked AFTER self is created,
        so after the "root" GASSupplierOrder is created
        """

        #WAS: INTERGAS 2
        log.debug("Planning %s for items=%s, frequency=%s" % (self, n_items, frequency))

        #Planning new orders
        for num in range(1, n_items+1):  #to iterate between 1 to _repeat_items

            #plan order
            plan_obj = self.clone()

            # planning
            plan_obj.root_plan = self

            r_q = frequency*num
            if self.delivery and self.delivery.date:
                r_dd = self.delivery.date
            else:
                r_dd = None

            #TODO: withdrawal appointment

            # Set date for open, close and delivery order
            plan_obj.datetime_start += timedelta(days=r_q)
            if plan_obj.datetime_end:
                plan_obj.datetime_end += timedelta(days=r_q)
            if r_dd:
                r_dd += timedelta(days=r_q)

            #Delivery appointment is None for a cloned order

            try:
                delivery, created = Delivery.objects.get_or_create(
                    date=r_dd,
                    place=self.delivery.place
                )
            except Delivery.MultipleObjectsReturned as e:
                log.error("Delivery.objects.get_or_create(%s, %s): returned more than one. Lookup parameters were date=%s, place=%s" % (
                    r_dd, self.delivery.place
                ))
                raise

            else:
                plan_obj.delivery = delivery

#WAS: INTERGAS 4

            #create order
            #COMMENT domthu: Don't understand why .save() not return true?
            #WAS: if plan_obj.save():
            #COMMENT fero: save() doesn't return True nor False.
            #COMMENT fero: it returns None. Django doc rules

            try:
                plan_obj.save()
            except Exception as e:
                log.debug("plan NOT created: item %s, r_q %s, start %s , end %s , delivery %s" % (
                    num, r_q, plan_obj.datetime_start,
                    plan_obj.datetime_end, plan_obj.delivery.date
                ))
                raise

#WAS: INTERGAS 5
            # Slight InterGAS optimization
            # Clone planned objects for related intergas order planning
            log.debug("InterGAS planned order creation optimization")
            if self.is_intergas:

                for related_intergas_order in self.get_complementary_intergas_orders():
                    intergas_plan_obj = related_intergas_order.clone()
                    intergas_plan_obj.datetime_start = plan_obj.datetime_start
                    intergas_plan_obj.datetime_end = plan_obj.datetime_end
                    intergas_plan_obj.delivery, created = Delivery.objects.get_or_create(
                        date=plan_obj.delivery.date,
                        place=plan_obj.delivery.place
                    )
                    print("XXX A")
                    try:
                        intergas_plan_obj.save()
                        log.debug("Related InterGAS planned order: %s " % intergas_plan_obj)
                    except Exception,e:
                        log.error("Related InterGAS planned order NOT created: pact %s, start %s , end %s , delivery %s" % (
                            intergas_plan_obj.pact, intergas_plan_obj.datetime_start,
                            intergas_plan_obj.datetime_end, intergas_plan_obj.delivery.date
                        ))
                        raise
            log.debug("CIAO XXX InterGAS planned order creation optimization")



    def delete_planneds(self):

        # Delete - Clean all previous planification
        planned_orders = self.get_planned_orders()
        log.debug("delete planned_orders: %s" % planned_orders)
        for order in planned_orders:

            #delete only prepared orders
            #WARNING LF! domthu: code is not aligned with comment above. Which one is right? is_active or not?
            if order.is_prepared or order.is_active:

#WAS: INTERGAS 3: not needed

                log.debug("AddOrderForm repeat delete previous_planned_orders: %s" % (order))
                order.delete()


    def get_intergas_pdf_data(self, requested_by=None):
        """Return PDF raw content to be rendered somewhere (email, or http)"""

        if not requested_by:
            requested_by = User.objects.get(username=settings.INIT_OPTIONS['su_username'])

        #print "order_list: %s" % self.get_intergas_orders()
        orderables_aggregate = GASSupplierOrderProduct.objects.none()
        for order in self.get_intergas_orders():
            orderables_aggregate = orderables_aggregate | order.orderable_products.filter(
                    gasmember_order_set__ordered_amount__gt=0
                    ).distinct()

        ordereds = self.ordered_products

        recProd, calc_tot_price, calc_prod_count = self.__get_intergas_pdfrecords_products(orderables_aggregate.order_by('gasstock__stock__product'))

        #families
        calc_fam_count = '?'

        context_dict = {
            'order' : self,
            'recProd' : recProd,
            'prod_count' : calc_prod_count,
            'total_amount' : calc_tot_price,
            'fam_count' : calc_fam_count,
            'have_note' : bool(self.allnotes.count() > 0),
            'user' : requested_by,
        }
        REPORT_TEMPLATE = "blocks/order_report_intergas/report.html"

        template = get_template(REPORT_TEMPLATE)
        context = Context(context_dict)
        html = template.render(context)
        result = StringIO.StringIO()
        #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1", "ignore")), result)
        pisadoc = pisa.pisaDocument(StringIO.StringIO(html.encode("utf-8", "ignore")), result)
        if not pisadoc.err:
            rv = result.getvalue()
        else:
            log.debug('Some problem while generate intergas pdf err: %s' % pisadoc.err)
            rv = None
        return rv

    def __get_intergas_pdfrecords_products(self, querySet):
        """Return records of rendered table fields."""

        records = []
        c = querySet.count()
        _actual_stock = -1
        _product = ''
        _price = 0
        _tot_gasmembers = 0
        _tot_amount = 0
        _tot_price = 0
        calc_tot_price = 0
        calc_prod_count = 0

        for el in querySet:
            if el.tot_price > 0:
                if ((_actual_stock != -1) & (_actual_stock != el.product.pk)):
                    records.append({
                       'product' : _product,
                       'price' : _price,
                       'tot_gasmembers' : _tot_gasmembers,
                       'tot_amount' : _tot_amount,
                       'tot_price' : _tot_price,
                    })
                if _actual_stock != el.product.pk:
                    calc_prod_count += 1
                    _actual_stock = el.product.pk
                    _product = el.product.name.encode('utf-8', "ignore")
                    _price = el.order_price
                    _tot_gasmembers = el.tot_gasmembers
                    _tot_amount = el.tot_amount
                    _tot_price = el.tot_price
                else:
                    #_product = el.product.name.encode('utf-8', "ignore")
                    _price += el.order_price
                    _tot_gasmembers += el.tot_gasmembers
                    _tot_amount += el.tot_amount
                    _tot_price += el.tot_price
                calc_tot_price += el.tot_price

        if _actual_stock != -1:
            records.append({
               'product' : _product,
               'price' : _price,
               'tot_gasmembers' : _tot_gasmembers,
               'tot_amount' : _tot_amount,
               'tot_price' : _tot_price,
            })
        return records, calc_tot_price, calc_prod_count

    #-----------------------------------------------#

    display_fields = (
        display.Resource(name="gas", verbose_name=_("GAS")),
        display.Resource(name="supplier", verbose_name=_("Supplier")),
        models.CharField(max_length=32, name="localized_current_state", verbose_name=_("Current state")),
        datetime_start, datetime_end, order_minimum_amount,
        delivery, display.Resource(name="referrer_person", verbose_name=_("Referrer")),
        withdrawal, display.Resource(name="withdrawal_referrer_person", verbose_name=_("Withdrawal referrer")),
    )

#register to revisions
if not reversion.is_registered(GASSupplierOrder):
    reversion.register(GASSupplierOrder)


#-------------------------------------------------------------------------------

class GASSupplierOrderProduct(models.Model, PermissionResource):
    """A Product (actually, a GASSupplierStock) available to GAS Members in the context of a given GASSupplierOrder.
    See `here <http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#ListinoFornitoreGasista>`__  for details (ITA only).

    """

    order = models.ForeignKey(GASSupplierOrder, related_name="orderable_product_set",verbose_name=_('order'))
    gasstock = models.ForeignKey(GASSupplierStock, related_name="orderable_product_set",verbose_name=_('gas stock'))
    # how many units of Product a GAS Member can request during this GASSupplierOrder
    # useful for Products with a low availability
    maximum_amount = PrettyDecimalField(null=True, blank=True, verbose_name = _('maximum amount'),
                        max_digits=8, decimal_places=2
    )
    # the price of the Product at the time the GASSupplierOrder was created
    initial_price = CurrencyField(verbose_name=_('initial price'))
    # the price of the Product at the time the GASSupplierOrder was sent to the Supplier
    order_price = CurrencyField(verbose_name=_('order price'))
    # the actual price of the Product (as resulting from the invoice)
    delivered_price = CurrencyField(null=True, blank=True,verbose_name=_('delivered price'))
    # how many items were actually delivered by the Supplier
    delivered_amount = PrettyDecimalField(null=True, blank=True, verbose_name = _('delivered amount'),
                        max_digits=8, decimal_places=2
    )

    #WAS: history = HistoricalRecords()

    class Meta:

        app_label = 'gas'
        verbose_name = _('gas supplier order product')
        verbose_name_plural = _('gas supplier order products')
        ordering = (
            'gasstock__stock__supplier__name',
            'gasstock__stock__supplier_category__sorting', #get suggestion from Orlando see if problems happen
            'gasstock__stock__product__category__name',
            'gasstock__stock__product__name'
        )

    def __unicode__(self):
        rv = ugettext('%(gasstock)s of order %(order)s') % { 'gasstock' : self.gasstock, 'order' : self.order}
        #if settings.DEBUG:
        #    rv += " [%s]" % self.pk
        return rv

    @property
    def has_changed(self):
        return self.initial_price != self.order_price

    # how many items of this kind were ordered (globally by the GAS)
    @property
    def tot_amount(self):
        # grab all GASMemberOrders related to this product and issued by members of the right GAS
        gmo_list = self.gasmember_order_set.values('ordered_amount')
        amount = 0
        for gmo in gmo_list:
            amount += gmo['ordered_amount']
        return amount

    @property
    def tot_gasmembers(self):
        return self.gasmember_order_set.count()

    @property
    def unconfirmed_orders(self):
        return self.gasmember_order_set.filter(is_confirmed=False).count()

    @property
    def tot_price(self):
        """Grab all GASMemberOrders related to this orderable product"""

        #INFO: i.e. if you want to optimize this method you could write:
        #INFO: self.gasmember_order_set.values('ordered_price', 'ordered_amount')
        #INFO: and compute tot_price in here.

        gmo_list = self.gasmember_order_set.all()
        tot = 0
        for gmo in gmo_list:
            tot += gmo.price_expected
        return tot

    @property
    def pact(self):
        return self.order.pact

    @property
    def des(self):
        return self.order.des

    @property
    def gas(self):
        return self.order.pact.gas

    @property
    def supplier(self):
        return self.order.supplier

    @property
    def product(self):
        return self.gasstock.product

    @property
    def stock(self):
        return self.gasstock.stock

    def save(self, *args, **kw):
        """Sef default initial price"""
        if not self.pk:
            self.initial_price = self.order_price
        if self.delivered_price is None:
            self.delivered_price = self.order_price

        super(GASSupplierOrderProduct, self).save(*args, **kw)

        # CASCADING set until GASMemberOrder
        if self.has_changed_price:
            log.debug('Price has changed for gsop (%s) [ %s--> %s]' %  (self.pk, self.order_price))
            for gmo in self.gasmember_order_set:
                #gmo.order_price = self.order_price
                gmo.note = ugettext("Price changed on %(date)s") % { 'date' : datetime.now() }
                gmo.save()


    @property
    def has_changed_price(self):
        try:
            gsop = GASSupplierOrderProduct.objects.get(pk=self.pk)
            if not gsop is None:
                return bool(self.order_price != gsop.order_price)
            else:
                return False
        except GASSupplierOrderProduct.DoesNotExist:
            return False

    #-------------- Authorization API ---------------#

    # Table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        # Who can add a new product to a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        try:
            order = context['order']
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.referrers
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)

    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can edit details of product associated with a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        allowed_users = self.order.referrers | self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete a product associated with a supplier order in a GAS ?
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        allowed_users = self.order.referrers | self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    def can_delegate(self, user):
        allowed_users = self.des.referrers | self.order.referrers | self.gas.tech_referrers | self.pact.referrers
        #WAS self.pact.gas_supplier_referrers  -->  self.pact.referrers
        return user in allowed_users

#register to revisions
if not reversion.is_registered(GASSupplierOrderProduct):
    reversion.register(GASSupplierOrderProduct)



class GASMemberOrder(models.Model, PermissionResource):

    """An order made by a GAS member in the context of a given GASSupplierOrder.

    See `here http://www.jagom.org/trac/REESGas/wiki/BozzaVocabolario#OrdineGasista`__  for details (ITA only).

    """

    purchaser = models.ForeignKey(GASMember, related_name="gasmember_order_set", null=False, blank=False,verbose_name=_('purchaser'))
    ordered_product = models.ForeignKey(GASSupplierOrderProduct, related_name="gasmember_order_set", null=False, blank=False,verbose_name=_('order product'))
    # price of the Product at order time
    ordered_price = CurrencyField(verbose_name=_('ordered price'))
    # how many Product units were ordered by the GAS member
    ordered_amount = PrettyDecimalField(null=False, blank=False, verbose_name = _('order amount'),
                        max_digits=6, decimal_places=2
    )
    # how many Product units were withdrawn by the GAS member
    withdrawn_amount = PrettyDecimalField(null=True, blank=True, verbose_name = _('widthdrawn amount'),
                        max_digits=6, decimal_places=2
    )
    # gasmember order have to be confirmed if GAS configuration allowed it
    is_confirmed = models.BooleanField(default=False,verbose_name=_('confirmed'))

    note = models.CharField(max_length=64, verbose_name=_('product note'), null=True, blank=True, help_text=_("GAS member can write some short message about this product for the producer"))

    #WAS: history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('GAS member order')
        verbose_name_plural = _('GAS member orders')
        unique_together = (('ordered_product', 'purchaser'),)

    def __unicode__(self):
        return u"Ordered product %(product)s by GAS member %(gm)s" % { 'product' : self.product, 'gm': self.gasmember }

    def confirm(self):
        #log.debug("Confirming the GAS member order #%d" % (self.pk))
        self.is_confirmed = True

    @property
    def has_changed(self):
        return self.ordered_product.order_price != self.ordered_price

    @property
    def price_expected(self):
        """Total expected to pay fot this order.

        The price is computed using order_price which is
        the last snapshot of the price for a product in an order.
        """

        #QUESTION: have we to use self.ordered_price instead of self.ordered_product.order_price?
        #ANSWER: NO. ordered_price is a copy of the price of the ordered_product when gasmember ordered it.

        #FIXME: needed for new families
        if self.withdrawn_amount == FAKE_WITHDRAWN_AMOUNT:
            return 0
        return self.ordered_product.order_price * self.ordered_amount

    @property
    def gasmember(self):
        return self.purchaser

    @property
    def product(self):
        return self.ordered_product.product

    @property
    def stock(self):
        return self.ordered_product.stock

    @property
    def gasstock(self):
        return self.ordered_product.gasstock

    @property
    def supplier(self):
        return self.ordered_product.supplier

    @property
    def email(self):
        return self.purchaser.email

    @property
    def order(self):
        """GASSupplierOrder this GASMemberOrder belongs to."""
        return self.ordered_product.order

    @property
    def des(self):
        return self.order.des

    @property
    def gas(self):
        """Which GAS this order belongs"""
        return self.purchaser.gas

    @property
    def pact(self):
        """GASSupplierOrderPact this GASMemberOrder belongs to."""
        return self.ordered_product.order.pact

    # Workflow management

    @property
    def workflow(self):
        return get_workflow(self)

    @workflow.setter
    def workflow(self, value=None):
        raise AttributeError(ugettext("Workflow for specific GASMemberOrder is not allowed. Just provide a default order workflow for your GAS"))

    def forward(self, user):
        """Apply default transition"""
        state = get_state(self)
        transition = DefaultTransition.objects.get(workflow=self.workflow, state=state).transition
        do_transition(self, transition, user)

    def save(self, *args, **kw):

        # Delete a GAS Member order if amount == 0
        if not self.ordered_amount:
            return self.delete()

        #Duplicate Entry. Retrieve data from database
        if not self.pk:
            YetExist = GASMemberOrder.objects.filter(ordered_product=self.ordered_product, purchaser=self.purchaser)
            if YetExist and YetExist.count() > 0:
                self.pk = YetExist[0].pk

        if not self.workflow:
            # Set default workflow
            w = self.gas.config.default_workflow_gasmember_order
            set_workflow(self, w)

        #If the GAS's member do not have to confirm is order auto set the flag
        if self.purchaser.gas.config.gasmember_auto_confirm_order:
            self.is_confirmed = True

        return super(GASMemberOrder, self).save(*args, **kw)

    #-------------- Authorization API ---------------#

    # Table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        # Who can issue an order *to* a GAS ?
        # *  members of that GAS
        try:
            order = context['order']
            allowed_users = order.gas.members
            return user in allowed_users
        except KeyError:
            raise WrongPermissionCheck('CREATE', cls, context)

    # Row-level EDIT permission
    def can_edit(self, user, context):
        # Who can modify an order placed by a GAS member ?
        # * the member itself (of course)
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        allowed_users = self.purchaser | self.order.referrers | self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    # Row-level DELETE permission
    def can_delete(self, user, context):
        # Who can delete an order placed by a GAS member ?
        # * the member itself (of course)
        # * order referrers (if any)
        # * referrers for the pact the order is placed against
        # * GAS administrators
        allowed_users = self.purchaser | self.order.referrers | self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    def can_delegate(self, user):
        allowed_users = self.des.referrers | self.order.referrers | self.gas.tech_referrers | self.pact.referrers
        return user in allowed_users

    #---------------------------------------------------#

#register to revisions
if not reversion.is_registered(GASMemberOrder):
    reversion.register(GASMemberOrder)


class Appointment(models.Model):
    """
    A base, abstract model class meant to factor out fields common to appointment-like models
    (i.e.  meetings, events, ..)
    """

    objects = AppointmentManager()

    class Meta:
        abstract = True

#-------------------------------------------------------------------------------#
# Model Archive API

    def is_active(self):
        """
        Return `True` if the Appointment is to be considered as 'active'; `False` otherwise.
        """
        return self in Appointment.objects.future()

    def is_archived(self):
        """
        Return `True` if the Appointment is to be considered as 'archived'; `False` otherwise.
        """
        return not self.is_active()

#-------------------------------------------------------------------------------#


class Delivery(Appointment, PermissionResource):

    """
    A delivery appointment, i.e. an event where one or more Suppliers deliver goods
    associated with SupplierOrders issued by a given GAS (or Retina of GAS).
    """

    place = models.ForeignKey(Place,
        related_name="delivery_set",
        help_text=_("where the order will be delivered by supplier"),
        verbose_name=_('place')
    )
    date = models.DateTimeField(
        help_text=_("when the order will be delivered by supplier"),
        verbose_name=_('date')
    )

    #WAS: history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')

    def __unicode__(self):
        return u"%(date)s %(at)s %(place)s" % {
            'date':long_date(self.date).capitalize(),
            'at': AT,
            'place':self.place
        }

    @property
    def gas_list(self):
        """
        Return a QuerySet containing all GAS sharing this delivery appointment.
        """
        pacts = GASSupplierSolidalPact.objects.filter(order_set__in=self.order_set.all())
        return GAS.objects.filter(pact_set__in = pacts)

    #-------------------------------------------------------------------------------#
    # Referrers API

    @property
    def referrers(self):
        """
        Return all users being referrers for this delivery appointment.
        """
        # retrieve 'delivery referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_DELIVERY, delivery=self)
        # retrieve all Users having this role
        return pr.get_users()

    @property
    def persons(self):
        return self.referrers_people


#-------------------------------------------------------------------------------#

    #-------------- Authorization API ---------------#

    # COMMENT-fero: now we do not use authoriazion API on this model.
    # we have to make some consideration for deliveries shared on more than one order

    # Table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        # TODO: REVIEW NEEDED see below (Withdrawal.can_create)
        # Who can schedule a new delivery appointment for a GAS ?
        # * pact referrers (all)
        # * order referrers (all, if any)
        # * GAS administrators

        # TODO: order referres: ticket www.jagom.org/trac/reesgas/ticket/185
        # add.. "evryone is referrer for one active order in GAS

        allowed_users = User.objects.none()
        try:
            # gas context
            gas = context['gas']
            allowed_users = gas.supplier_referrers | gas.tech_referrers
        except KeyError:
            try:
                # TODO: ticket www.jagom.org/trac/reesgas/ticket/185
                # order context
                order = context['order']
                raise NotImplementedError("can_create withdrawal in order")
                allowed_users = order.referrers | order.gas.supplier_referrers | order.gas.tech_referrers
            except KeyError:
                raise WrongPermissionCheck('CREATE', cls, context)

        return user in allowed_users

    # Row-level EDIT permission
    def can_edit(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can modify a delivery appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any)
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators
        # 3) ELSE:
        #     * DES administrators

        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()
        if len(associated_orders) == 1:
            order = associated_orders[0]
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.referrers
        #WAS order.pact.gas_supplier_referrers  -->  order.pact.referrers
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers

        return user in allowed_users

    # Row-level DELETE permission
    def can_delete(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can delete a delivery appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any)
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators
        # 3) ELSE:
        #     * DES administrators
        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()
        if len(associated_orders) == 1:
            order = associated_orders[0]
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.referrers
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers

        return user in allowed_users


    #---------------------------------------------------#

#register to revisions
if not reversion.is_registered(Delivery):
    reversion.register(Delivery)



class Withdrawal(Appointment, PermissionResource):
    """
    A wihtdrawal appointment, i.e. an event where a GAS (or Retina of GAS) distribute
    to their GASMembers goods they ordered issuing GASMemberOrders to the GAS/Retina.
    """

    place = models.ForeignKey(Place,
        related_name="withdrawal_set",
        help_text=_("where the order will be withdrawn by GAS members")
    )

    date = models.DateTimeField(
        help_text=_("when the order will be withdrawn by GAS members")
    )

    # a Withdrawal appointment usually span a time interval
    start_time = models.TimeField(default="18:00", help_text=_("when the withdrawal will start"))
    end_time = models.TimeField(default="22:00", help_text=_("when the withdrawal will end"))

    #WAS: history = HistoricalRecords()

    class Meta:
        app_label = 'gas'
        verbose_name = _('wihtdrawal')
        verbose_name_plural = _('wihtdrawals')

    def __unicode__(self):
        return u"%(on)s %(date)s %(from)s %(start_time)s %(to)s %(end_time)s %(at)s %(place)s" % {
                    'start_time':self.start_time.strftime("%H:%M"),
                    'end_time':self.end_time.strftime("%H:%M"),
                    'date':long_date(self.date).capitalize(),
                    'place':self.place,
                    'on' : ON, 'at': AT,
                    'from' : FROM, 'to': TO,
        }


    @property
    def gas_list(self):
        """
        Return a QuerySet containing all GAS sharing this withdrawal appointment.

        """
        pacts = GASSupplierSolidalPact.objects.filter(order_set__in=self.order_set.all())
        return GAS.objects.filter(pact_set__in = pacts)

    #-------------------------------------------------------------------------------#
    # Referrers API

    @property
    def referrers(self):
        """
        Return all users being referrers for this wihtdrawal appointment.
        """
        # retrieve 'wihtdrawal referrer' parametric role for this order
        pr = ParamRole.get_role(GAS_REFERRER_WITHDRAWAL, withdrawal=self)
        # retrieve all Users having this role
        return pr.get_users()

    @property
    def persons(self):
        return self.referrers_people


#-------------------------------------------------------------------------------#


    #-------------- Authorization API ---------------#

    # COMMENT-fero: now we do not use authoriazion API on this model.
    # we have to make some consideration for withdrawals shared on more than one order

    # Table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        # Who can schedule a new withdrawal appointment for a GAS ?
        # * pact referrers (all)
        # * GAS administrators

        # TODO: order referres: ticket www.jagom.org/trac/reesgas/ticket/185
        # add.. "evryone is referrer for one active order in GAS

        allowed_users = User.objects.none()
        try:
            # gas context
            gas = context['gas']
            allowed_users = gas.supplier_referrers | gas.tech_referrers
        except KeyError:
            try:
                # TODO: ticket www.jagom.org/trac/reesgas/ticket/185
                # order context
                order = context['order']
                raise NotImplementedError("can_create withdrawal in order")
                allowed_users = order.referrers | order.gas.supplier_referrers | order.gas.tech_referrers
            except KeyError:
                raise WrongPermissionCheck('CREATE', cls, context)

        return user in allowed_users

    # Row-level EDIT permission
    def can_edit(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can modify a withdrawal appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any)
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators
        # 3) ELSE:
        #     * DES administrators
        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()
        if len(associated_orders) == 1:
            order = associated_orders[0]
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.referrers
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers

        return user in allowed_users

    # Row-level DELETE permission
    def can_delete(self, user, context):
        # TODO: REVIEW NEEDED see above (can_create)
        # Who can delete a withdrawal appointment ?
        # (remember that they can be shared among orders and GASs)
        # 1) If only one supplier order is currently associated with this appointment:
        #     * order referrers (if any)
        #     * referrers for the pact that order is placed against
        #     * GAS administrators
        # 2) If more than one order is currently associated with this appointment,
        #    but they belogns to the same GAS:
        #     * GAS administrators
        # 3) ELSE:
        #     * DES administrators
        allowed_users = User.objects.none()
        associated_orders = self.order_set.all()
        if len(associated_orders) == 1:
            order = associated_orders[0]
            allowed_users = order.referrers | order.gas.tech_referrers | order.pact.referrers
        elif len(self.gas_list) == 1:
            gas = self.gas_list[0]
            allowed_users = gas.tech_referrers

        return user in allowed_users

    #---------------------------------------------------#

#register to revisions
if not reversion.is_registered(Withdrawal):
    reversion.register(Withdrawal)

