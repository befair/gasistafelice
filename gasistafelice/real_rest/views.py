#from django.http import HttpResponse
#from django.contrib.auth.decorators import login_required
#from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import User

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

import serializers as my_serializers

from base.models import Person, Contact
from gas.models import GAS, GASMember
from supplier.models import Supplier

#--------------------------------------------------------------------------------
# REST API

class PersonCreateReadView(ListCreateAPIView):

    model = Person

class PersonReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    model = Person
    serializer_class = my_serializers.PersonSerializer

class GASReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    model = GAS
    serializer_class = my_serializers.GASSerializer

class SupplierReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    model = Supplier
    serializer_class = my_serializers.SupplierSerializer

class GASMemberReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    #TODO: controllo sui permessi (solo su questa... non sulle altre...!)

    model = GASMember
    serializer_class = my_serializers.GASMemberSerializer

