#WAS: INTERGAS 0
#    intergas = forms.BooleanField(label=_('This order is InterGAS?'), required=False)
#    intergas_grd = forms.MultipleChoiceField(label=_('gas'), choices=GAS.objects.none(), required=False, widget=forms.CheckboxSelectMultiple)
#WAS: INTERGAS 1
#            gas_list = None
#            if pacts.count() == 1:
#                #log.debug("AddOrderForm only one pact %s" % pacts)
#                gas_list = [(gas.pk, gas.name) for gas in one_pact.supplier.gas_list]
#            else:
#                gas_list = [(gas.pk, gas.name) for gas in GAS.objects.all()]
#            self.fields['intergas_grd'].choices = gas_list
#WAS: INTERGAS 2
#        #InterGAS
#        _intergas_pacts = None
#        _intergas_number = None
#        _intergas = self.cleaned_data['intergas']
#        if bool(_intergas):

#            #interGAS gas list
#            _intergas_gas_list = self.cleaned_data['intergas_grd']
#            if _intergas_gas_list and _intergas_gas_list.count > 0:
#                #Add the default order's gas in the list
#                _intergas_pacts = set() #GAS.objects.none()
#                #_intergas_pacts.add(self.instance.pact)
#                for g in _intergas_gas_list:
#                    if int(g) != self.instance.gas.pk:
#                        log.debug("AddOrderForm intergas find %s another PACT:%s" % (g, self.instance.gas.pk))
#                        #_intergas_gas = _intergas_gas | GAS.objects.get(pk=g)
#                        x_g = GAS.objects.get(pk=g)
#                        if x_g:
#                            #retrieve the existing pact for this gas for this supplier. If exist.
#                            x_p = GASSupplierSolidalPact.objects.filter(gas=x_g, supplier=self.instance.pact.supplier)
#                            if x_p and x_p.count()>0:
#                                _intergas_pacts.add(x_p[0])
#                                if x_p.count() > 1:
#                                    log.debug("AddOrderForm intergas INCONGRUITY looking for gas %s and supplier %s" % (x_g, self.instance.pact.supplier))
#                #if _intergas_pacts.count() == 1:
#                if len(_intergas_pacts) == 0:
#                    #Not valid InterGAS almost 2 GAS to be an interGAS's order
#                    _intergas_pacts = None
#                else:
#                    #interGAS aggregation number
#                    _intergas_number = get_group_id()
#                    log.debug("AddOrderForm intergas --> (%s) another PACTs:%s" % (_intergas_number, _intergas_pacts))

#                    #Set instance as InterGAS
#                    self.instance.group_id = _intergas_number
#            #WAS: _intergas_orders = GASSupplierOrder.objects.none()
#            _intergas_orders = set()
#            if _intergas_pacts and _intergas_number:
#                log.debug("AddOrderForm interGAS OPEN for other GAS")
#                #Repeat this order for the overs GAS
#                for other_pact in _intergas_pacts:
#                    other_order = GetNewOrder(self.instance, other_pact)
#                    if other_order:
#                        #COMMENT domthu: Don't understand why .save() not return true?
#                        #WAS: if other_order.save():
#                        other_order.save()
#                        if other_order.pk:
#                            log.debug("repeat created another order: %s " % (other_order))
#                            _intergas_orders.add(other_order)
#                        else:
#                            log.debug("repeat another NOT created: pact %s, start %s , end %s , delivery %s" % (other_order.pact, other_order.datetime_start, other_order.datetime_end, other_order.delivery.date))
#WAS: INTERGAS 3
#                        #if InterGAS delete relative group_id others orders.
#                        if order.group_id and order.group_id > 0:
#                            #COMMENT: do it in Models with def delete(self, *args, **kw)?
#                            planed_intergas_orders = GASSupplierOrder.objects.filter(group_id=order.group_id)
#                            if planed_intergas_orders and planed_intergas_orders.count() >0:
#                                for intergas_order in planed_intergas_orders:
#                                    log.debug("AddOrderForm repeat delete intergas_previous_planed_orders: %s" % (intergas_order))
#                                    intergas_order.delete()
#WAS: INTERGAS 4
#                    #get new interGAS number if needed
#                    if _intergas_orders:
#                        x_obj.group_id = get_group_id()
#WAS: INTERGAS 5
#                        #InterGAS
#                        if _intergas_orders:
#                            for other_order in _intergas_orders:
#                                try:
#                                    other_order.datetime_start = x_obj.datetime_start
#                                    other_order.datetime_end = x_obj.datetime_end
#                                    other_order.delivery.date = x_obj.delivery.date
#                                    x_other_obj = GetNewOrder(other_order, None)
#                                    if x_other_obj:
#                                        #COMMENT domthu: Don't understand why .save() not return true?
#                                        if x_other_obj.save():
#                                            log.debug("another repeat created order: %s " % (x_other_obj))
#                                        else:
#                                            log.debug("another repeat NOT created: pact %s, start %s , end %s , delivery %s" % (x_other_obj.pact, x_other_obj.datetime_start, x_other_obj.datetime_end, x_other_obj.delivery.date))
#                                except Exception,e:
#                                    log.debug("another repeat NOT created order ERROR: %s " % (e))
#WAS: INTERGAS 6
#                            , ('intergas', 'intergas_grd')


