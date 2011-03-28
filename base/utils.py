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
        role = Role.objects.create(name=name, gas=gas, supplier=supplier, delivery=delivery, withdrawal=withdrawal, order=order)
    except IntegrityError:
        return False
    return role