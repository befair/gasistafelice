#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import User

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

import serializers as my_serializers

from gf.base.models import Person, Contact
from gf.gas.models import GAS, GASMember
from gf.supplier.models import Supplier

# REST API
#--------------------------------------------------------------------------------

class PersonCreateReadView(ListCreateAPIView):

    model = Person

class PersonReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    model = Person
    serializer_class = my_serializers.PersonSerializer
    queryset = Person.objects.all() #TODO HURRY

@login_required
def get_user_person(request):
    """
    Return serialized info for person bound to authed user
    """
    return PersonReadUpdateDeleteView.as_view()(request, pk=request.user.person.pk)

#--------------------------------------------------------------------------------

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
    queryset = Person.objects.all() #TODO HURRY

