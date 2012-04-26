
Aggiornare dalla 0.8 alla 0.9
=============================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Installare il modulo django-ajax-selects con pip install django-ajax-selects
2. Eliminare lo storico del GASConfig con::

    # echo "DROP TABLE gas_historicalgasconfig CASCADE" | python manage.py dbshell
    # python manage.py syncdb


Buon divertimento!
Luca `fero` Ferroni
