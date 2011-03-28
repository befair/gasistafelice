from permissions.models import Role as BaseRole
from gasistafelice.base import Role 

def register_role(name, gas=None, supplier=None, delivery=None, withdrawal=None, order=None):
    """Registers a Role with passed parameters. Returns the new
    Role if the registration was successfully, otherwise False.    

    **Parameters:**

    name
        a (unique) name for the Role 
    gas
        the GAS (if any) the Role is related to 
    supplier
        the Supplier (if any) the Role is related to
    delivery
        the Delivery appointment (if any) the Role is related to
    withdrawal
        the Withdrawal appointment (if any) the Role is related to
    order
        the GASSuplierOrder (if any) the Role is related to
    """

# just a trivial extension of the `register_role` function found in `django-permissions`,
# taking into account the additional parameters for the constructor of our custom `Role` model class     
    try:
        # check if a BaseRole with the passed name already exists in the DB
        base_role = BaseRole.objects.get(name=name) 
    except BaseRole.DoesNotExist:  
        # if not, create it      
        base_role = BaseRole.objects.create(name=name)
    finally:
        try: 
            # check if a Role with the passed parameters already exists in the DB
            role = Role.objects.get(base_role=base_role, gas=gas, supplier=supplier, delivery=delivery, withdrawal=withdrawal, order=order)
            return False
        except Role.DoesNotExist:
            role = Role.objects.create(base_role=base_role, gas=gas, supplier=supplier, delivery=delivery, withdrawal=withdrawal, order=order)
            return role
        
            