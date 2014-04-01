from rest_framework import serializers

from base.models import Person, Contact
from gas.models.base import GAS, GASMember, GASSupplierStock
from gas.models.order import GASSupplierOrder, GASMemberOrder, Delivery, GASSupplierOrderProduct
from supplier.models import Product, SupplierStock, Supplier

class ProductSerializer(serializers.ModelSerializer):
    mu = serializers.CharField()
    pu = serializers.CharField()
    class Meta:
        model = Product

class SupplierStockSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = SupplierStock

class GASSupplierOrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = GASSupplierOrderProduct

class GASSupplierStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = GASSupplierStock

class DeliverySerializer(serializers.ModelSerializer):
    place = serializers.CharField()

    class Meta:
        model = Delivery

class GASMemberPkListingField(serializers.RelatedField):

    def to_native(self, value):
        return value.pk

class OrderSerializer(serializers.ModelSerializer):

    gasstock_set = GASSupplierStockSerializer(many=True)
    stocks = SupplierStockSerializer(many=True)
    delivery = DeliverySerializer()
    supplier = GASMemberPkListingField()

    class Meta:
        model = GASSupplierOrder

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('flavour', 'value', 'is_preferred')

class GASSerializer(serializers.ModelSerializer):

    des = serializers.CharField()
    open_orders = OrderSerializer(many=True)

    class Meta:
        model = GAS
        fields = ('id', 'name', 'id_in_des', 'logo', 'des', 'open_orders')
        
class SupplierSerializer(serializers.ModelSerializer):

    contact_set = ContactSerializer(many=True)
    certifications = serializers.RelatedField(many=True)
    seat = serializers.RelatedField()

    class Meta:
        model = Supplier

class PersonSerializer(serializers.ModelSerializer):

    contact_set = ContactSerializer(many=True)
    gas_list = GASSerializer(many=True)
    gasmembers = GASMemberPkListingField(many=True)
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

class GASMemberOrderSerializer(serializers.ModelSerializer):

    ordered_product = GASSupplierOrderProductSerializer()

    class Meta:
        model = GASMemberOrder

class CashInfoSerializer(serializers.CharField):
    """
    Cash are sensible info
    """

    def __init__(self, *args, **kw):

        return super(CashInfoSerializer, self).__init__(*args, **kw)

class GASMemberSerializer(serializers.ModelSerializer):

    economic_state = serializers.CharField()
    balance = serializers.FloatField()
    total_basket = serializers.FloatField()
    total_basket_to_be_delivered = serializers.FloatField()
    basket = GASMemberOrderSerializer(many=True)
    basket_to_be_delivered = GASMemberOrderSerializer(many=True)

    class Meta:
        model = GASMember
        fields = (
            'id', 'gas', 'person', 'membership_fee_payed',  
            'is_suspended', 'suspend_datetime', 'suspend_auto_resume',
            'balance', 'total_basket', 'total_basket_to_be_delivered',
            'economic_state', 'basket', 'basket_to_be_delivered'
        )
        
