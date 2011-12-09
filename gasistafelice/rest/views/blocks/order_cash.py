"""View for block details specialized for a GASSupplierOrder"""

from django.utils.translation import ugettext as _, ugettext_lazy as _lazy

from gasistafelice.rest.views.blocks import details
from gasistafelice.gas.forms import cash as order_cash_forms

from gasistafelice.consts import INCOME, EXPENSE
from gasistafelice.rest.views.blocks.base import ResourceBlockAction

import logging
log = logging.getLogger(__name__)

class Block(details.Block):

    BLOCK_NAME = "order_cash"
    BLOCK_VALID_RESOURCE_TYPES = ["order"]

#    def _get_edit_form_class(self):
#        # TODO:  TOVERIFY fero
#        """GASSupplierOrder is an atom, so we have to return a formset"""
#        #return order_cash_forms.form_class_factory_for_request(self.request, base=order_forms.CashOrderForm)
#        return order_cash_forms.CashOrderForm()

#    def get_description(self):
#        return _("%(name)s's GAS memberships") % {
#            'name' : self.resource.order.report_name,
#        }

#DOMTHU
#    def total_amount(self):
#    def tot_price(self):
#    def tot_amount(self):
#    def tot_gasmembers(self):
#    def tot_curtail(self):
#    def payment(self):
#    def payment_urn(self):


#state
#tot_price 1
#invoice_amount 2 
#payment 3

#invoice_note

#unsolved Multiplechoice 
#total 1 2 3  (ordinati + fatture + pagati)

#amount_to_pay textbox


    def _get_user_actions(self, request):

        user_actions = super(Block, self)._get_user_actions(request)

        refs = [] #request.resource.cash_referrers

        # REMOVE programmatically managed transitions
        for action in ['make_unpaid']:
            try:
                user_actions.remove(action)
            except ValueError:
                pass

        #FIXME: disabled actions until implemented
        try:
            user_actions.remove('close_and_send')
        except ValueError:
            pass

        if refs and request.user in refs:
            log.debug("--------------       order_details actions refs.count() = %s- " % (refs.count()))

            user_actions += [
                #TODO: ECO 1 way for inserting economic data popup form for order.delivery_cost set
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=INCOME, verbose_name=_("Ricezione fattura"),
                    popup_form=False,
                ),

                #TODO: ECO popup form for order --Payment(s)
                ResourceBlockAction(
                    block_name = self.BLOCK_NAME,
                    resource = request.resource,
                    name=EXPENSE, verbose_name=_("Pagamento ordine(i)"),
                    popup_form=False,
                ),

            ]

#DOMTHU:            act_configure = ResourceBlockAction(
#                    block_name = self.BLOCK_NAME,
#                    resource = request.resource,
#                    name="configure", verbose_name=_("Configure"),
#                    popup_form=True,
#                    url = reverse('admin:gas_gasconfig_change', args=(request.resource.config.pk,)) 
#            )

#DOMTHU:            for i,act in enumerate(user_actions):
#                # Change URL for action EDIT, insert "configure" action
#                if act.name == EDIT:
#                   act.url = reverse('admin:gas_gas_change', args=(request.resource.pk,)) 
#                   user_actions.insert(i+1, act_configure)
#                   break

        return user_actions


