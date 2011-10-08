import django.dispatch

order_state_update = django.dispatch.Signal(providing_args=["transition"])

gmo_price_update = django.dispatch.Signal(providing_args=["old_price", "new_price"])
gmo_product_erased = django.dispatch.Signal(providing_args=[])

gasstock_product_disabled = django.dispatch.Signal(providing_args=[])
gasstock_product_enabled = django.dispatch.Signal(providing_args=[])


