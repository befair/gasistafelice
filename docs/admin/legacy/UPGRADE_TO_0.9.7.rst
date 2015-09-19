
Aggiornare dalla 0.9.x alla 0.9.7
=================================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Installare il modulo south con pip install south
2. Eliminare i file initial_data.json: find . -name initial_data.json | xargs rm
3. Eseguire ./manage.py syncdb
4. Eseguire la prima finta migrazione di south con ./manage.py migrate gas 0001 --fake
5. Eseguire le migrazioni dello schema del database con ./manage.py migrate gas --no-initial-data

A questo punto si verifichera' un errore, che si puo' risolvere sostituendo nel file
``lib/python2.7/site-packages/current_user/models.py`` 
il metodo __init__ della classe CurrentUserField con:

.. sourcecode:: python

    def __init__(self, **kwargs):
        kwargs['to'] = User
        kwargs['null'] = True
        super(CurrentUserField, self).__init__(**kwargs)


Update 20120230 may be require the same source code modification for file 
``src/django-pro-history/current_user/models.py``


Ripetere il punto 5 e 
buon divertimento!
Luca `fero` Ferroni
