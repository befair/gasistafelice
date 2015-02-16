from django.db.models.query import QuerySet
from datetime import date

from django.contrib.contenttypes.models import ContentType  
from workflows.models import StateObjectRelation

class GASMemberQuerySet(QuerySet):
    # TODO: refactor here some GASMemberManager objects
    pass

class OrderQuerySet(QuerySet):
    
    def get_by_state(self, name):
        """
        Return a QuerySet containing all ``GASSupplierOrder``s whose current state is named as ``name``.
        
        Note that is not the same as retrieving every ``GASSupplierOrder`` having a given state,
        since different model instances may be associated to different workflows, and states belonging to 
        different workflows are different even if they are named the same way.          
        """
        order_ct = ContentType.objects.get_for_model(self.model)
        sors = StateObjectRelation.objects.filter(content_type=order_ct, state__name=name)
        orders = self.filter(pk__in=[sor.content_id for sor in sors])
        return orders
    
    def prepared(self):
        return self.get_by_state('Prepared')

    def open(self):
        return self.get_by_state('Open')

    def closed(self):
        return self.get_by_state('Closed')
    
    def on_completion(self):
        return self.get_by_state('On completion')
    
    def finalized(self):
        return self.get_by_state('Finalized')
    
    def unpaid(self):
        return self.get_by_state('Unpaid')
    
    def delivered(self):
        return self.get_by_state('Delivered')
    
    def archived(self):
        return self.get_by_state('Archived')
    
    def canceled(self):
        return self.get_by_state('Canceled')
            
#-------------------------------------------------------------------------------

class AppointmentQuerySet(QuerySet):

    def future(self):
        """
        Return a QuerySet containing all appointments scheduled for today or for a future date.
        """
        return self.filter(date__gte=date.today())

    def past(self):
        """
        Return a QuerySet containing all past appointments.
        """
        return self.filter(date__lt=date.today())
