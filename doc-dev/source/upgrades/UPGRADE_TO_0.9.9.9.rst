
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

>>> def update_balance_current(ledger_entry): 
>>>    lg_entries_previous = ledger_entry.account.ledger_entries.order_by('entry_id')
>>>    # Redo all increments as a security mesaure to avoid
>>>    # tampering of last balance, but ... do we really need this 
>>>    # security measure? Is it ok to redo basing on amount because balance
>>>    # is an inherited attribute
>>>    for entry in lg_entries_previous:
>>>        if entry.entry_id <= ledger_entry.entry_id:
>>>            ledger_entry.balance_current = (ledger_entry.balance_current or 0) + entry.amount
>>>     ledger_entry.save()
>>>
>>> from simple_accounting.models import LedgerEntry, Account
>>> for ac in Account.objects.all():
>>>     for lg in ac.ledger_entries.order_by('entry_id'):
>>>         update_balance_current(lg)
>>>         print("%(entry_id)s %(amount)s %(balance_current)s" % lg.__dict__)
>>>


buon divertimento!
Luca `fero` Ferroni
