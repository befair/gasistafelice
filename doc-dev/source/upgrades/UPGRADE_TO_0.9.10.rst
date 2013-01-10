
Aggiornare dalla 0.9.8 alla 0.9.10
==================================

Oltre a sincronizzare il proprio codice sorgente con 
https://github.com/feroda/gasistafelice

# git clone https://github.com/feroda/gasistafelice.git

nell'aggiornamento a questa versione è necessario:

1. Aggiungere il campo `balance_current` 
2. Popolare il campo `balance_current` per tutte le voci del registro registrate

Esempio per il vostro sistema:

Punto 0:

./manage.py syncdb

Punto 1:

- sqlite3
# echo ALTER TABLE simple_accounting_ledgerentry ADD COLUMN "balance_current" DECIMAL | ./manage.py dbshell

- postgresql
# echo ALTER TABLE simple_accounting_ledgerentry ADD COLUMN "balance_current" numeric(10, 4) | ./manage.py dbshell

Punto 2:

# ./manage.py shell

>>> from simple_accounting.models import LedgerEntry, Account
>>> for ac in Account.objects.all():
>>>     for lg in ac.ledger_entries.order_by('entry_id'):
>>>         lg.save()
>>>         print("%(entry_id)s %(amount)s %(balance_current)s" % lg.__dict__)


buon divertimento!
Luca `fero` Ferroni
