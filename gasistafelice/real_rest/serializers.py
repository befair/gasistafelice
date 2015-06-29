from rest_framework import serializers

from gf.base.models import Person, Contact, Place
from gf.gas.models.base import GAS, GASMember, GASSupplierStock
from gf.gas.models.order import GASSupplierOrder, GASMemberOrder, Delivery, GASSupplierOrderProduct
from gf.supplier.models import Product, SupplierStock, Supplier
from simple_accounting.models import LedgerEntry, Transaction

class ProductSerializer(serializers.ModelSerializer):
    mu = serializers.CharField()
    pu = serializers.CharField()
    class Meta:
        model = Product

class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__unicode__', 'producer', 'category')

class SupplierStockSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()

    class Meta:
        model = SupplierStock
        fields = (
            'id', 'product', 'image', 'price', 'code', 'amount_available',
            'units_minimum_amount', 'units_per_box', 'detail_minimum_amount',
            'detail_step', 'delivery_notes', 'supplier', 'supplier_category'
        )

class GASSupplierOrderProductSerializer(serializers.ModelSerializer):

    stock = SupplierStockSerializer()

    class Meta:
        model = GASSupplierOrderProduct

class GASSupplierStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = GASSupplierStock

class DeliverySerializer(serializers.ModelSerializer):
    place = serializers.CharField()

    class Meta:
        model = Delivery

class QSListingField(serializers.ReadOnlyField):

    def to_representation(self, value):
        return map(lambda x: x.pk, value.all())

class QSUnicodeModelField(serializers.ReadOnlyField):

    def to_representation(self, value):
        return map(lambda x: unicode(x), value.all())

class PkModelField(serializers.ReadOnlyField):

    def to_representation(self, value):
        return value.pk

class NameModelField(serializers.ReadOnlyField):

    def to_representation(self, value):
        return getattr(value, 'name', None)

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('flavour', 'value', 'is_preferred')

class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Place
        fields = ('name', 'address', 'zipcode', 'city', 'province', 'lat', 'lon')

class SimpleSupplierSerializer(serializers.ModelSerializer):

    seat = SeatSerializer(read_only=True)

    class Meta:
        model = Supplier
        fields = ('id', 'name', 'seat', 'preferred_phone_address', 'preferred_email_address')

class SupplierSerializer(SimpleSupplierSerializer):

    contact_set = ContactSerializer(many=True)
    certifications = QSUnicodeModelField(read_only=True) #TODO... read_only?!?

    class Meta:
        model = Supplier

class OrderSerializer(serializers.ModelSerializer):

    orderable_product_set = GASSupplierOrderProductSerializer(many=True)
    #TODO TOREMOVE gasstock_set = GASSupplierStockSerializer(many=True)
    stocks = SupplierStockSerializer(many=True)
    delivery = DeliverySerializer()
    supplier = SimpleSupplierSerializer(read_only=True)

    class Meta:
        model = GASSupplierOrder

class OrderInfoSerializer(serializers.ModelSerializer):

    delivery = DeliverySerializer()
    supplier = serializers.CharField()
    current_state = NameModelField()

    class Meta:
        model = GASSupplierOrder
        fields = (
            'id', 'delivery', 'supplier',
            '__unicode__', 'current_state'
        )

class SimpleGASSerializer(serializers.ModelSerializer):

    des = serializers.CharField()
    headquarter = SeatSerializer()

    class Meta:
        model = GAS
        fields = ('id', 'name', 'id_in_des', 'logo', 'des', 'headquarter')

class GASSerializer(SimpleGASSerializer):
    open_orders = OrderSerializer(many=True)

    class Meta:
        model = GAS
        fields = ('id', 'name', 'id_in_des', 'logo', 'des', 'headquarter')

class PersonSerializer(serializers.ModelSerializer):

    contact_set = ContactSerializer(many=True)
    gas_list = SimpleGASSerializer(many=True)
    gasmembers = QSListingField(read_only=True) #TODO... read_only?!?
    suppliers = SupplierSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            'id', 'name', 'surname', 'display_name',
            'ssn', 'avatar', 'website', 'contact_set',
            'user', 'gasmembers', 'gas_list', 'suppliers'
        )

#---------------------------------------------------------------------------------
# GAS Member serializers.
# Should be used carefully in views because they holds sensitive informations
class PlainGASSupplierOrderProductSerializer(serializers.ModelSerializer):

    stock = SupplierStockSerializer()
    order = OrderInfoSerializer()

    class Meta:
        model = GASSupplierOrderProduct


class GASMemberOrderSerializer(serializers.ModelSerializer):

    ordered_product = PlainGASSupplierOrderProductSerializer()

    class Meta:
        model = GASMemberOrder
        fields = (
            'id', 'ordered_product', 'ordered_price',
            'ordered_amount', 'is_confirmed', 'note'
        )

class CashInfoSerializer(serializers.CharField):
    """
    Cash are sensible info
    """

    def __init__(self, *args, **kw):

        return super(CashInfoSerializer, self).__init__(*args, **kw)

class GASMemberSerializer(serializers.ModelSerializer):

    gas = SimpleGASSerializer()
    # WAS: economic_state = serializers.CharField()
    balance = serializers.FloatField()
    total_basket = serializers.FloatField()
    total_basket_to_be_delivered = serializers.FloatField()
    basket = GASMemberOrderSerializer(many=True)
    basket_to_be_delivered = GASMemberOrderSerializer(many=True)
    open_orders = OrderSerializer(many=True)

    class Meta:
        model = GASMember
        fields = (
            'id', 'gas', 'person', 'membership_fee_payed',
            'is_suspended', 'suspend_datetime', 'suspend_auto_resume',
            'balance', 'total_basket', 'total_basket_to_be_delivered',
            'basket', 'basket_to_be_delivered', 'open_orders'
        )

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'kind', 'description')

class LedgerEntrySerializer(serializers.ModelSerializer):

    transaction = TransactionSerializer()

    class Meta:
        model = LedgerEntry
        fields = (
            'id', 'date', 'account', 'transaction', 'amount'
        )
class GASMemberCashSerializer(serializers.ModelSerializer):

    gas = SimpleGASSerializer()
    economic_movements = LedgerEntrySerializer(many=True)

    class Meta:
        model = GASMember
        fields = (
            'id', 'gas', 'cash_info', 'membership_fee_payed',
            'economic_movements'
        )

