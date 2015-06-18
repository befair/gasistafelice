Aggiornare dalla 0.11 alla 0.12
===============================

#. Installare `django-reversion`::

    $ pip install -r requirements/base.py

#. **OPZIONALE**: rimuovere le tabelle relative a django-pro-history::

    decommentare le righe dalla 11 alla 41, relative alla cancellazione della history, nel file `gasistafelice/gas/migrations/0004_auto__del_historicalgasmemberorder__del_historicalgasconfig__del_histo.py`
 
    ATTENZIONE: questo rimuoverà tutti dati esistenti relativi alla history.

#. Sincronizzare il database::

    $ ./manage.py syncdb

#. Eseguire le migrazioni del database::

    $ ./manage.py migrate gas 0003 --fake

    $ ./manage.py migrate gas --no-initial-data

    $ ./manage.py migrate reversion --no-initial-data

#. Registrare le revisioni iniziali dei modelli::

    $ ./manage.py createinitialrevisions 

enjoy!

Marko
