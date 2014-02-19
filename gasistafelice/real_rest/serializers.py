from rest_framework import serializers

from base.models import Person, Contact
from gas.models.base import GAS, GASMember, GASSupplierStock
from gas.models.order import GASSupplierOrder
from supplier.models import Product, SupplierStock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
class SupplierStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierStock
class GASSupplierStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = GASSupplierStock

class OrderSerializer(serializers.ModelSerializer):

    gasstock_set = GASSupplierStockSerializer(many=True)
    stocks = SupplierStockSerializer(many=True)
    #products = ProductSerializer(many=True)

    class Meta:
        model = GASSupplierOrder

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('flavour', 'value', 'is_preferred')

class GASSerialiser(serializers.ModelSerializer):

    des = serializers.CharField()
    orders = OrderSerializer(many=True)

    class Meta:
        model = GAS
        fields = ('id', 'name', 'id_in_des', 'logo', 'des', 'orders')
        
class GASMemberSerialiser(serializers.ModelSerializer):

    economic_state = serializers.CharField()
    balance = serializers.FloatField()
    total_basket = serializers.FloatField()
    total_basket_to_be_delivered = serializers.FloatField()

    class Meta:
        model = GASMember
        fields = (
            'id', 'gas', 'person', 'membership_fee_payed',  
            'is_suspended', 'suspend_datetime', 'suspend_auto_resume',
            'balance', 'total_basket', 'total_basket_to_be_delivered',
            'economic_state'
        )
        
class PersonSerializer(serializers.ModelSerializer):

    contact_set = ContactSerializer(many=True)
    gas_list = GASSerialiser(many=True)
    #suppliers = SupplierSerialiser(many=True)
    gasmembers = GASMemberSerialiser(many=True)

    class Meta:
        model = Person
        fields = (
            'id', 'name', 'surname', 'display_name', 
            'ssn', 'avatar', 'website', 'contact_set',
            'user', 'gasmembers', 'gas_list',  
        )


