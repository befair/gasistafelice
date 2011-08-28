from django.db.models.query import QuerySet

class RoleQuerySet(QuerySet):
    """
    A custom QuerySet intended to ease the task of retrieving specific subsets 
    of parametric roles' model instances.    
    """

    def active(self):
        """
        Filter the current QuerySet including only 'active' parametric roles.
        The semantic (what is meant by 'active') and implementation 
        (how to retrieve active roles) is delegated to specific models.
        """
        active_roles_list = [role for role in self if role.is_active()]
        qs = self.filter(pk__in=[obj.pk for obj in active_roles_list])
        return qs

    def archived(self):
        """
        Filter the current QuerySet including only 'archived' parametric roles.
        The semantic (what is meant by 'archived') and implementation 
        (how to retrieve archived roles) is delegated to specific models.
        """
        archived_roles_list = [role for role in self if role.is_archived()]
        qs = self.filter(pk__in=[obj.pk for obj in archived_roles_list])
        return qs

