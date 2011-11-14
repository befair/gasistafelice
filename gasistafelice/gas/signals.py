import django.dispatch

order_state_update = django.dispatch.Signal(providing_args=["transition"])
order_open = django.dispatch.Signal(providing_args=[])

gmo_price_update = django.dispatch.Signal(providing_args=[])
gmo_product_erased = django.dispatch.Signal(providing_args=[])

gasstock_product_disabled = django.dispatch.Signal(providing_args=[])
gasstock_product_enabled = django.dispatch.Signal(providing_args=[])


